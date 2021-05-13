#!/usr/bin/env python3

import requests
import numpy as np

symbol = 'btcusdt'

def get_price(symbol):
    responses = requests.get(
        f'http://api.huobi.pro/market/detail/merged?symbol={symbol}')
    responses = responses.json()
    price = responses['tick']['close']
    return price


if __name__ == '__main__':
    price = get_price(symbol)
    price = f'<span color="#c6ea0f">{price * 3.65:,.2f}</span>'
    print(price)
