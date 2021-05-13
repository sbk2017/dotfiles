#!/usr/bin/env python3

import requests

def getprice():
    link = 'https://api.coingecko.com/api/v3/coins/ethereum/tickers?exchange_ids=binance&page=1'
    req = requests.get(link).json()
    eth = req['tickers'][0]['last']
    return eth

if __name__ == '__main__':
    eth = getprice()
    print(f'<span color="#c6ea0f">{eth:,.2f}</span>')
