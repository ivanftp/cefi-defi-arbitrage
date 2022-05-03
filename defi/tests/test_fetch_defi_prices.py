import requests
import pytest


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2&amount=100000000000").json()],
    ids=["str_data"],
)
def test_eth_from_token_amount(test_data):
    # pull data from 1inch and test whether fromTokenAmount is a positive integer
    fromTokenAmount = test_data['fromTokenAmount']
    assert (fromTokenAmount.startswith('-') == False) and fromTokenAmount[1:].isdigit()


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2&amount=100000000000").json()],
    ids=["str_data"],
)
def test_eth_to_token_amount(test_data):
    # pull data from 1inch and test whether toTokenAmount is a positive integer
    toTokenAmount = test_data['toTokenAmount']
    assert (toTokenAmount.startswith('-') == False) and toTokenAmount[1:].isdigit()


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9&amount=100000000000").json()],
    ids=["str_data"],
)
def test_aave_from_token_amount(test_data):
    # pull data from 1inch and test whether fromTokenAmount is a positive integer
    fromTokenAmount = test_data['fromTokenAmount']
    assert (fromTokenAmount.startswith('-') == False) and fromTokenAmount[1:].isdigit()


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9&amount=100000000000").json()],
    ids=["str_data"],
)
def test_aave_to_token_amount(test_data):
    # pull data from 1inch and test whether toTokenAmount is a positive integer
    toTokenAmount = test_data['toTokenAmount']
    assert (toTokenAmount.startswith('-') == False) and toTokenAmount[1:].isdigit()


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x1f9840a85d5af5bf1d1762f925bdaddc4201f984&amount=100000000000").json()],
    ids=["str_data"],
)
def test_uni_from_token_amount(test_data):
    # pull data from 1inch and test whether fromTokenAmount is a positive integer
    fromTokenAmount = test_data['fromTokenAmount']
    assert (fromTokenAmount.startswith('-') == False) and fromTokenAmount[1:].isdigit()


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x1f9840a85d5af5bf1d1762f925bdaddc4201f984&amount=100000000000").json()],
    ids=["str_data"],
)
def test_uni_to_token_amount(test_data):
    # pull data from 1inch and test whether toTokenAmount is a positive integer
    toTokenAmount = test_data['toTokenAmount']
    assert (toTokenAmount.startswith('-') == False) and toTokenAmount[1:].isdigit()


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x514910771af9ca656af840dff83e8264ecf986ca&amount=100000000000").json()],
    ids=["str_data"],
)
def test_link_from_token_amount(test_data):
    # pull data from 1inch and test whether fromTokenAmount is a positive integer
    fromTokenAmount = test_data['fromTokenAmount']
    assert (fromTokenAmount.startswith('-') == False) and fromTokenAmount[1:].isdigit()


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x514910771af9ca656af840dff83e8264ecf986ca&amount=100000000000").json()],
    ids=["str_data"],
)
def test_link_to_token_amount(test_data):
    # pull data from 1inch and test whether toTokenAmount is a positive integer
    toTokenAmount = test_data['toTokenAmount']
    assert (toTokenAmount.startswith('-') == False) and toTokenAmount[1:].isdigit()


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x111111111117dc0aa78b770fa6a738034120c302&amount=100000000000").json()],
    ids=["str_data"],
)
def test_1inch_from_token_amount(test_data):
    # pull data from 1inch and test whether fromTokenAmount is a positive integer
    fromTokenAmount = test_data['fromTokenAmount']
    assert (fromTokenAmount.startswith('-') == False) and fromTokenAmount[1:].isdigit()


@pytest.mark.parametrize(
    "test_data",
    [requests.get("https://api.1inch.io/v4.0/1/quote?fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&toTokenAddress=0x111111111117dc0aa78b770fa6a738034120c302&amount=100000000000").json()],
    ids=["str_data"],
)
def test_1inch_to_token_amount(test_data):
    # pull data from 1inch and test whether toTokenAmount is a positive integer
    toTokenAmount = test_data['toTokenAmount']
    assert (toTokenAmount.startswith('-') == False) and toTokenAmount[1:].isdigit()
