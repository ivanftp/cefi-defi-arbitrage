import requests
import pytest


def is_float(item):
    try:
        float(item)
        return True
    except ValueError:
        return False


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.binance.com/api/v1/depth?symbol=ETHUSDT").json()],
    ids=["str_data"],
)
def test_eth_bid_price(test_data):
    # pull data from binance and test whether bid price and volume is a float
    bid = test_data['bids'][0]
    assert is_float(bid[0]) and is_float(bid[1])


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.binance.com/api/v1/depth?symbol=ETHUSDT").json()],
    ids=["str_data"],
)
def test_eth_ask_price(test_data):
    # pull data from binance and test whether ask price and volume is a float
    ask = test_data['asks'][0]
    assert is_float(ask[0]) and is_float(ask[1])


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.binance.com/api/v1/depth?symbol=AAVEUSDT").json()],
    ids=["str_data"],
)
def test_aave_bid_price(test_data):
    # pull data from binance and test whether bid price and volume is a float
    bid = test_data['bids'][0]
    assert is_float(bid[0]) and is_float(bid[1])


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.binance.com/api/v1/depth?symbol=AAVEUSDT").json()],
    ids=["str_data"],
)
def test_aave_ask_price(test_data):
    # pull data from binance and test whether ask price and volume is a float
    ask = test_data['asks'][0]
    assert is_float(ask[0]) and is_float(ask[1])


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.binance.com/api/v1/depth?symbol=UNIUSDT").json()],
    ids=["str_data"],
)
def test_uni_bid_price(test_data):
    # pull data from binance and test whether bid price and volume is a float
    bid = test_data['bids'][0]
    assert is_float(bid[0]) and is_float(bid[1])


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.binance.com/api/v1/depth?symbol=UNIUSDT").json()],
    ids=["str_data"],
)
def test_uni_ask_price(test_data):
    # pull data from binance and test whether ask price and volume is a float
    ask = test_data['asks'][0]
    assert is_float(ask[0]) and is_float(ask[1])


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.binance.com/api/v1/depth?symbol=LINKUSDT").json()],
    ids=["str_data"],
)
def test_link_bid_price(test_data):
    # pull data from binance and test whether bid price and volume is a float
    bid = test_data['bids'][0]
    assert is_float(bid[0]) and is_float(bid[1])


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.binance.com/api/v1/depth?symbol=LINKUSDT").json()],
    ids=["str_data"],
)
def test_link_ask_price(test_data):
    # pull data from binance and test whether ask price and volume is a float
    ask = test_data['asks'][0]
    assert is_float(ask[0]) and is_float(ask[1])


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.binance.com/api/v1/depth?symbol=1INCHUSDT").json()],
    ids=["str_data"],
)
def test_1inch_bid_price(test_data):
    # pull data from binance and test whether bid price and volume is a float
    bid = test_data['bids'][0]
    assert is_float(bid[0]) and is_float(bid[1])


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.binance.com/api/v1/depth?symbol=1INCHUSDT").json()],
    ids=["str_data"],
)
def test_1inch_ask_price(test_data):
    # pull data from binance and test whether ask price and volume is a float
    ask = test_data['asks'][0]
    assert is_float(ask[0]) and is_float(ask[1])
