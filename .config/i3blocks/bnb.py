#!/usr/bin/env python3

import requests

def getprice():
    link = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=binancecoin&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h'
    req = requests.get(link).json()
    price = f"<span color='#c6ea0f'>{req[0]['current_price']:,.2f}</span>"
    if req[0]['price_change_percentage_24h'] > 0:
        changes = f"<span color='#3BB92D'>{req[0]['price_change_percentage_24h']:,.2f}%</span>"
    else:
        changes = f"<span color='#F7555E'>{req[0]['price_change_percentage_24h']:,.2f}%</span>"
    return price + '  ' + changes

if __name__ == '__main__':
    bnb = getprice()
    print(bnb)
