from arbitrage.app import calculate_profit
import json


def test_calculate_profit():
    # test outputs from calculate_profit() function have the correct values and types
    cex_buy_price = {'ETHUSDT': 2789.26, '1INCHUSDT': 1.146, 'AAVEUSDT': 144.9, 'UNIUSDT': 7.06, 'LINKUSDT': 11.2}
    dex_sell_price = {'AAVEUSDT': 144.50244696042617, '1INCHUSDT': 1.1421777116809815, 'LINKUSDT': 11.159650326998841,
                      'ETHUSDT': 2790.980980194445, 'UNIUSDT': 7.038055503576642}
    result = json.loads(calculate_profit(cex_buy_price, dex_sell_price, 'cex_buy_price', 'dex_sell_price'))
    assert (type(result['0']['profitable_trade']) == bool) \
           and (result['0']['crypto'] in cex_buy_price) \
           and (type(result['0']['trade_size']) == int) \
           and result['0']['cex_buy_price'].startswith('$') \
           and result['0']['dex_sell_price'].startswith('$') \
           and type(result['0']['profit']) == str
