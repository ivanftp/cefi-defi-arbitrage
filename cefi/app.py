import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import aiohttp
import json


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
        self.prices = {"BTCUSDT": None, "ETHUSDT": None, "LUNAUSDT": None, "BNBUSDT": None}

    @staticmethod
    async def fetch(session, url):
        async with session.get(url) as resp:
            return await resp.json()

    async def get_prices(self):
        while True:
            await asyncio.sleep(1)
            loop = asyncio.get_event_loop()
            async with aiohttp.ClientSession() as session:
                tasks = []
                for symbol in self.prices:
                    url = 'https://api.binance.com/api/v1/ticker/price?symbol={0}'.format(symbol)
                    tasks.append(loop.create_task(self.fetch(session, url)))
                for result in asyncio.as_completed(tasks):
                    try:
                        price_dict = await result
                        self.prices[price_dict['symbol']] = price_dict['price']
                    except aiohttp.client_exceptions.ClientConnectorError as e:
                        print(e)


process = BackgroundProcess()


@app.on_event('startup')
async def app_startup():
    asyncio.create_task(process.get_prices())


@app.get("/")
def root():
    return process.prices


if __name__ == '__main__':
    uvicorn.run(app, port=3000, host='0.0.0.0')

