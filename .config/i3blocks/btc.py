#!/usr/bin/env python3

import requests
import numpy as np
import btc_chart
import sys

symbol = 'btcusdt'


def get_price(symbol):
    responses = requests.get(
        f'http://api.huobi.pro/market/detail/merged?symbol={symbol}')
    responses = responses.json()
    price = responses['tick']['close']
    return price


def get_changes(symbol):
    price = get_price(symbol)
    history = requests.get(
        f'http://api.huobi.pro/market/history/kline?period=60min&size=200&symbol={symbol}')
    data = history.json()['data']
    data = np.array([x['close'] for x in data])
    price_avg = data.mean()
    changes = (price - price_avg) / price_avg * 100
    return changes


def chart():
    btc_chart.run_chart()


def main():
    price = get_price(symbol)
    price = f'<span color="#c6ea0f">{price:,.2f}</span>'
    changes = get_changes(symbol)
    if changes < 0:
        _changes = f'<span color="#F7555E">[{changes:.2f}%]</span>'
    elif changes > 0:
        _changes = f'<span color="#3BB92D">{changes:.2f}%</span>'
    else:
        _changes = f'<span color="#CCCCCC">{changes:.2f}%</span>'

    print(price + '  ' + _changes)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        chart()
        main()
    else:
        main()
