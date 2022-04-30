import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

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

    async def get_prices(self):
        while True:
            await asyncio.sleep(1)
            for symbol in self.prices:
                url = 'https://api.binance.com/api/v1/ticker/price?symbol={0}'.format(symbol)
                response = requests.request("GET", url)
                self.prices[symbol] = response.json()["price"]


process = BackgroundProcess()


@app.on_event('startup')
async def app_startup():
    asyncio.create_task(process.get_prices())


@app.get("/")
def root():
    return process.prices


if __name__ == '__main__':
    uvicorn.run(app, port=3000, host='0.0.0.0')

