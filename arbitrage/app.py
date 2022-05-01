from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import aiohttp
import pandas as pd
import numpy as np
from babel.numbers import format_currency


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BackgroundProcess:
    def __init__(self):
        self.cex_url = 'http://localhost:3000/'
        self.dex_url = 'http://localhost:3001/'
        self.cex_buy_price = {}
        self.dex_buy_price = {}
        self.cex_sell_price = {}
        self.dex_sell_price = {}
        self.df_buy_cex_sell_dex = pd.DataFrame()
        self.df_buy_dex_sell_cex = pd.DataFrame()

    @staticmethod
    async def fetch(session, url, exchange, order):
        async with session.get(url) as resp:
            return await resp.json(), exchange, order

    async def check_arbitrage(self):
        while True:
            await asyncio.sleep(0.5)
            loop = asyncio.get_event_loop()
            async with aiohttp.ClientSession() as session:
                tasks = []
                tasks.append(loop.create_task(self.fetch(session, self.cex_url + 'buy', 'cex', 'buy')))
                tasks.append(loop.create_task(self.fetch(session, self.cex_url + 'sell', 'cex', 'sell')))
                tasks.append(loop.create_task(self.fetch(session, self.dex_url + 'buy', 'dex', 'buy')))
                tasks.append(loop.create_task(self.fetch(session, self.dex_url + 'sell', 'dex', 'sell')))
                for result in asyncio.as_completed(tasks):
                    try:
                        price_dict, exchange, order = await result
                        if exchange == 'cex':
                            if order == 'buy':
                                self.cex_buy_price = price_dict
                            elif order == 'sell':
                                self.cex_sell_price = price_dict
                        elif exchange == 'dex':
                            if order == 'buy':
                                self.dex_buy_price = price_dict
                            elif order == 'sell':
                                self.dex_sell_price = price_dict
                    except aiohttp.client_exceptions.ClientConnectorError as e:
                        print(e)
                self.df_buy_cex_sell_dex = pd.concat([pd.DataFrame.from_dict(self.cex_buy_price, orient='index', columns=['cex_buy_price']),
                                                      pd.DataFrame.from_dict(self.dex_sell_price, orient='index', columns=['dex_sell_price'])], axis=1)
                self.df_buy_cex_sell_dex['trade_size'] = (100000 / self.df_buy_cex_sell_dex['cex_buy_price']).astype(int)
                self.df_buy_cex_sell_dex['raw_profit'] = ((self.df_buy_cex_sell_dex['dex_sell_price'] - self.df_buy_cex_sell_dex['cex_buy_price']) * self.df_buy_cex_sell_dex['trade_size']).round(2)
                self.df_buy_cex_sell_dex['profit'] = self.df_buy_cex_sell_dex['raw_profit'].apply(lambda x: format_currency(x, currency="USD", locale="en_US"))
                self.df_buy_cex_sell_dex['profitable_trade'] = np.where(self.df_buy_cex_sell_dex['raw_profit'] > 0, True, False)
                self.df_buy_cex_sell_dex.drop('raw_profit', 1, inplace=True)
                self.df_buy_dex_sell_cex = pd.concat([pd.DataFrame.from_dict(self.dex_buy_price, orient='index', columns=['dex_buy_price']),
                                                      pd.DataFrame.from_dict(self.cex_sell_price, orient='index', columns=['cex_sell_price'])], axis=1)
                self.df_buy_dex_sell_cex['trade_size'] = (100000 / self.df_buy_dex_sell_cex['dex_buy_price']).astype(int)
                self.df_buy_dex_sell_cex['raw_profit'] = ((self.df_buy_dex_sell_cex['cex_sell_price'] - self.df_buy_dex_sell_cex['dex_buy_price']) * self.df_buy_dex_sell_cex['trade_size']).round(2)
                self.df_buy_dex_sell_cex['profit'] = self.df_buy_dex_sell_cex['raw_profit'].apply(lambda x: format_currency(x, currency="USD", locale="en_US"))
                self.df_buy_dex_sell_cex['profitable_trade'] = np.where(self.df_buy_dex_sell_cex['raw_profit'] > 0, True, False)
                self.df_buy_dex_sell_cex.drop('raw_profit', 1, inplace=True)


process = BackgroundProcess()


@app.on_event('startup')
async def app_startup():
    asyncio.create_task(process.check_arbitrage())


@app.get("/")
def root():
    return process.df_buy_cex_sell_dex.to_string()


if __name__ == '__main__':
    uvicorn.run(app, port=3002, host='0.0.0.0')