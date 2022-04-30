import requests
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
        self.symbols = ["ETHUSDT", "AAVEUSDT", "UNIUSDT", "LINKUSDT", "1INCHUSDT"]
        self.buy_price = {}
        self.sell_price = {}

    @staticmethod
    async def fetch(session, url, symbol):
        async with session.get(url) as resp:
            return await resp.json(), symbol

    async def get_prices(self):
        while True:
            await asyncio.sleep(1)
            loop = asyncio.get_event_loop()
            async with aiohttp.ClientSession() as session:
                tasks = []
                for symbol in self.symbols:
                    url = 'https://api.binance.com/api/v1/depth?symbol={0}'.format(symbol)
                    tasks.append(loop.create_task(self.fetch(session, url, symbol)))
                for result in asyncio.as_completed(tasks):
                    try:
                        price_dict, symbol = await result
                        self.buy_price[symbol] = float(price_dict['asks'][0][0])  # Assuming enough volume on Binance, we can buy at the lowest ask
                        self.sell_price[symbol] = float(price_dict['bids'][0][0])  # Assuming enough volume on Binance, we can sell at the highest bid
                    except aiohttp.client_exceptions.ClientConnectorError as e:
                        print(e)


process = BackgroundProcess()


@app.on_event('startup')
async def app_startup():
    asyncio.create_task(process.get_prices())


@app.get("/buy")
def root():
    return process.buy_price


@app.get("/sell")
def root():
    return process.sell_price


if __name__ == '__main__':
    uvicorn.run(app, port=3000, host='0.0.0.0')

