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
def test_bid_price(test_data):
    bid = test_data['bids'][0]
    assert is_float(bid[0]) and is_float(bid[1])


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.binance.com/api/v1/depth?symbol=ETHUSDT").json()],
    ids=["str_data"],
)
def test_ask_price(test_data):
    ask = test_data['asks'][0]
    assert is_float(ask[0]) and is_float(ask[1])
