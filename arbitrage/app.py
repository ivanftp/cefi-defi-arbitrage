from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import aiohttp


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


process = BackgroundProcess()


@app.on_event('startup')
async def app_startup():
    asyncio.create_task(process.check_arbitrage())


@app.get("/")
def root():
    return str(process.cex_buy_price) + ' ' + str(process.dex_buy_price) + ' '  + str(process.cex_sell_price) + ' '  + str(process.dex_sell_price)


if __name__ == '__main__':
    uvicorn.run(app, port=3002, host='0.0.0.0')