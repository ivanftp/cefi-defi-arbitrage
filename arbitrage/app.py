import pandas as pd
import numpy as np
from babel.numbers import format_currency
from flask import Flask, render_template
import requests


app = Flask(__name__, template_folder="templates")

cex_url = 'http://localhost:3000/'
dex_url = 'http://localhost:3001/'


@app.route("/")
def home():
    # dashbaord with live prices, profits and arbitrage opportunities
    return render_template("home.html")


def calculate_profit(buy_price, sell_price, buy_column_name, sell_column_name):
    df = pd.concat(
        [pd.DataFrame.from_dict(buy_price, orient='index', columns=[buy_column_name]).round(3),
         pd.DataFrame.from_dict(sell_price, orient='index', columns=[sell_column_name]).round(3)], axis=1)
    df['trade_size'] = (100000 / df[buy_column_name]).astype(int)  # Calculate trade size assuming $100k USDT per trade
    df['raw_profit'] = (
            (df[sell_column_name] - df[buy_column_name]) *
            df['trade_size']).round(2)  # Calculate profit by multiplying price difference with trade size
    df['profit'] = df['raw_profit'].apply(
        lambda x: format_currency(x, currency="USD", locale="en_US"))
    df['profitable_trade'] = np.where(df['raw_profit'] > 0, True, False)  # Determine if arbitrage opportunity exists
    df.drop('raw_profit', 1, inplace=True)  # Drop unused columns
    df.index.name = 'crypto'
    df = df.reset_index()
    df[sell_column_name] = df[sell_column_name].apply(lambda x: '$' + str(x))  # Format sell prices to include currency symbol
    df[buy_column_name] = df[buy_column_name].apply(lambda x: '$' + str(x))  # Format buy prices to include currency symbol
    return df.T.to_json()


@app.route("/buy_cex_sell_dex")
def buy_cex_sell_dex():
    try:
        cex_buy_price = requests.get(cex_url + 'buy').json()  # get buy prices from cefi app
        dex_sell_price = requests.get(dex_url + 'sell').json()  # get sell prices from defi app
        return calculate_profit(cex_buy_price, dex_sell_price, 'cex_buy_price', 'dex_sell_price')
    except Exception as e:
        print(e)


@app.route("/buy_dex_sell_cex")
def buy_dex_sell_cex():
    try:
        cex_sell_price = requests.get(cex_url + 'sell').json()  # get sell prices from cefi app
        dex_buy_price = requests.get(dex_url + 'buy').json()  # get buy prices from defi app
        return calculate_profit(dex_buy_price, cex_sell_price, 'dex_buy_price', 'cex_sell_price')
    except Exception as e:
        print(e)



if __name__ == '__main__':
    app.run(debug=True, port=3002, host='0.0.0.0')
