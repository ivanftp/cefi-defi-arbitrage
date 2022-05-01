import pandas as pd
import numpy as np
from babel.numbers import format_currency
from flask import Flask, render_template
import json
import requests


app = Flask(__name__, template_folder="templates")

cex_url = 'http://localhost:3000/'
dex_url = 'http://localhost:3001/'


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/buy_cex_sell_dex")
def buy_cex_sell_dex():
    try:
        cex_buy_price = requests.get(cex_url + 'buy').json()
        dex_sell_price = requests.get(dex_url + 'sell').json()

        df_buy_cex_sell_dex = pd.concat(
            [pd.DataFrame.from_dict(cex_buy_price, orient='index', columns=['cex_buy_price']).round(3),
             pd.DataFrame.from_dict(dex_sell_price, orient='index', columns=['dex_sell_price']).round(3)], axis=1)
        df_buy_cex_sell_dex['trade_size'] = (100000 / df_buy_cex_sell_dex['cex_buy_price']).astype(int)
        df_buy_cex_sell_dex['raw_profit'] = (
                (df_buy_cex_sell_dex['dex_sell_price'] - df_buy_cex_sell_dex['cex_buy_price']) *
                 df_buy_cex_sell_dex['trade_size']).round(2)
        df_buy_cex_sell_dex['profit'] = df_buy_cex_sell_dex['raw_profit'].apply(
            lambda x: format_currency(x, currency="USD", locale="en_US"))
        df_buy_cex_sell_dex['profitable_trade'] = np.where(df_buy_cex_sell_dex['raw_profit'] > 0, True, False)
        df_buy_cex_sell_dex.drop('raw_profit', 1, inplace=True)
        df_buy_cex_sell_dex.index.name = 'crypto'
        df_buy_cex_sell_dex = df_buy_cex_sell_dex.reset_index()
        df_buy_cex_sell_dex['dex_sell_price'] = df_buy_cex_sell_dex['dex_sell_price'].apply(lambda x: '$' + str(x))
        df_buy_cex_sell_dex['cex_buy_price'] = df_buy_cex_sell_dex['cex_buy_price'].apply(lambda x: '$' + str(x))
    except Exception as e:
        print(e)

    return df_buy_cex_sell_dex.T.to_json()


@app.route("/buy_dex_sell_cex")
def buy_dex_sell_cex():
    try:
        cex_sell_price = requests.get(cex_url + 'sell').json()
        dex_buy_price = requests.get(dex_url + 'buy').json()

        df_buy_dex_sell_cex = pd.concat(
            [pd.DataFrame.from_dict(dex_buy_price, orient='index', columns=['dex_buy_price']).round(3),
             pd.DataFrame.from_dict(cex_sell_price, orient='index', columns=['cex_sell_price']).round(3)], axis=1)
        df_buy_dex_sell_cex['trade_size'] = (100000 / df_buy_dex_sell_cex['dex_buy_price']).astype(int)
        df_buy_dex_sell_cex['raw_profit'] = (
                (df_buy_dex_sell_cex['cex_sell_price'] - df_buy_dex_sell_cex['dex_buy_price']) *
                df_buy_dex_sell_cex['trade_size']).round(2)
        df_buy_dex_sell_cex['profit'] = df_buy_dex_sell_cex['raw_profit'].apply(
            lambda x: format_currency(x, currency="USD", locale="en_US"))
        df_buy_dex_sell_cex['profitable_trade'] = np.where(df_buy_dex_sell_cex['raw_profit'] > 0, True, False)
        df_buy_dex_sell_cex.drop('raw_profit', 1, inplace=True)
        df_buy_dex_sell_cex.index.name = 'crypto'
        df_buy_dex_sell_cex = df_buy_dex_sell_cex.reset_index()
        df_buy_dex_sell_cex['dex_buy_price'] = df_buy_dex_sell_cex['dex_buy_price'].apply(lambda x: '$'+str(x))
        df_buy_dex_sell_cex['cex_sell_price'] = df_buy_dex_sell_cex['cex_sell_price'].apply(lambda x: '$' + str(x))
    except Exception as e:
        print(e)

    return df_buy_dex_sell_cex.T.to_json()


if __name__ == '__main__':
    app.run(debug=True, port=3002, host='0.0.0.0')
