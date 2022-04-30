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
        # To account for DEX volume and slippage, trade size assumed to be approximately $100k USDT
        self.symbols = ["ETHUSDT", "AAVEUSDT", "UNIUSDT", "LINKUSDT", "1INCHUSDT"]
        self.buy_price = {}
        self.sell_price = {}
        self.buy_url = {
            "ETHUSDT": "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2&amount=100000000000",
            "AAVEUSDT": "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9&amount=100000000000",
            "UNIUSDT": "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x1f9840a85d5af5bf1d1762f925bdaddc4201f984&amount=100000000000",
            "LINKUSDT": "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x514910771af9ca656af840dff83e8264ecf986ca&amount=100000000000",
            "1INCHUSDT": "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x111111111117dc0aa78b770fa6a738034120c302&amount=100000000000"}

        self.sell_url = {
            "ETHUSDT": "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2&toTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&amount=36000000000000000000",
            "AAVEUSDT": "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9&toTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&amount=657000000000000000000",
            "UNIUSDT": "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0x1f9840a85d5af5bf1d1762f925bdaddc4201f984&toTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&amount=13700000000000000000000",
            "LINKUSDT": "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0x514910771af9ca656af840dff83e8264ecf986ca&toTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&amount=8630000000000000000000",
            "1INCHUSDT": "https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0x111111111117dc0aa78b770fa6a738034120c302&toTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&amount=81500000000000000000000"}

    @staticmethod
    async def fetch(session, url, symbol, order):
        async with session.get(url) as resp:
            return await resp.json(), symbol, order

    async def get_prices(self):
        while True:
            await asyncio.sleep(1)
            loop = asyncio.get_event_loop()
            async with aiohttp.ClientSession() as session:
                tasks = []
                for symbol in self.symbols:
                    sell_url = self.sell_url[symbol]
                    tasks.append(loop.create_task(self.fetch(session, sell_url, symbol, 'sell')))
                    buy_url = self.buy_url[symbol]
                    tasks.append(loop.create_task(self.fetch(session, buy_url, symbol, 'buy')))
                for result in asyncio.as_completed(tasks):
                    try:
                        price_dict, symbol, order = await result
                        if order == 'sell':
                            self.sell_price[symbol] = (int(price_dict['toTokenAmount'])/int(price_dict['fromTokenAmount'])) * 1e12
                        elif order == 'buy':
                            self.buy_price[symbol] = (int(price_dict['fromTokenAmount'])/int(price_dict['toTokenAmount'])) * 1e12
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
    uvicorn.run(app, port=3001, host='0.0.0.0')

