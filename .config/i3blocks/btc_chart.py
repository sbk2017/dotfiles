#!/usr/bin/env python3

import requests
import pandas as pd
from dearpygui.core import *
from dearpygui.simple import *
import time
from datetime import datetime
import numpy as np
# import pandas as pd


def t_conv(isotime):
    cm = datetime.fromtimestamp(isotime)
    dt = mpdates.date2num(cm)
    return cm.timestamp()


def nf(number : float) -> str:
    # number format 
    return f'{number:,.2f}'



def mv(x : list, w : int) -> list:
    return np.convolve(x, np.ones(w), 'valid') / w


def quit_callback(sender, data):
    stop_dearpygui()


def get_data(period='1min'):
    symbol = 'btcusdt'
    weblinks = f'http://api.huobi.pro/market/history/kline?period={period}&size=100&symbol={symbol}'
    data = requests.get(weblinks).json()['data']
    df = pd.DataFrame(data)
    df = df.sort_values(by=['id'])
    df.reset_index(drop=True)
    df['mv7'] = df.iloc[:,2].rolling(window=7).mean()
    # close = [x['close'] for x in data.json()['data']]
    # _open = [x['open'] for x in data.json()['data']]
    # high = [x['high'] for x in data.json()['data']]
    # low = [x['low'] for x in data.json()['data']]
    # _date = [x['id'] for x in data.json()['data']]
    # tm = [x['id'] for x in data.json()['data']]
    # highest = f'{max(close):,.2f}'
    # lowest = f'{min(close):,.2f}'
    # average = f'{np.mean(close):,.2f}'
    # mintime = time.ctime(min(tm))
    # maxtime = time.ctime(max(tm))
    # ft = datetime.strptime(mintime.split()[-2], '%H:%M:%S')
    # lt = datetime.strptime(maxtime.split()[-2], '%H:%M:%S')
    # dif = lt - ft
    # hrs = dif.seconds / 3600  # the data time in hrs
    # tablerows = [highest, lowest, average]
    # chart_data = {'date': _date, 'open': _open,
    #               'high': high, 'low': low, 'close': close}
    # return hrs, mintime, maxtime, tablerows, chart_data
    return df


def chart_update(sender, data):
    # print(sender, data)
    # hrs, mintime, maxtime, tablerows, chart_data = get_data(sender)
    df = get_data(sender)
    clear_plot('plot')
    delete_series('plot', 'BTCUSDT')
    time.sleep(1)
    set_value('text', f'{sender} for last  hours') #{hrs:.2f}
    set_table_data('Data Table', [[nf(float(df['close'].tail(1))), nf(df['close'].max()), nf(df['close'].min()), nf(df['close'].mean())]])
    add_candle_series('plot',
                      "BTCUSDT",
                      date=list(df['id']),
                      opens=list(df['open']),
                      highs=list(df['high']),
                      lows=list(df['low']),
                      closes=list(df['close']),
                      # weight=.25,
                      )
    add_line_series('plot', 'MA', list(df['id']), list(df['mv7']),
                        color=[204, 0, 204])

def run_chart():
    # chart using DearPyGui
    df = get_data()
    add_additional_font('/home/sultan/.fonts/Exo-Regular.ttf', 18)
    set_main_window_size(850, 500)
    set_theme("Grey")
    with window('BTC chart'):
        # add_additional_font('FiraCode-SemiBold.ttf', 12)
        # set_global_font_scale(1.2)
        add_table('Data Table',
                  ['Price','Highest', 'lowest', 'avrage'],
                  height=50)
        add_row('Data Table', [nf(float(df['close'].tail(1))), nf(df['close'].max()), nf(df['close'].min()), nf(df['close'].mean())])
        add_label_text('text', color=[97, 236, 55])
        set_value('text', f'for last  hours') #{hrs:.2f}
        add_button('Quit', callback=quit_callback)
        add_same_line(spacing=10)
        add_button('1min', callback=chart_update)
        add_same_line(spacing=10)
        add_button('30min', callback=chart_update)
        add_same_line(spacing=10)
        add_button('60min', callback=chart_update)
        add_plot('plot', xaxis_time=True)
        add_candle_series('plot',
                          "BTCUSDT",
                          date=list(df['id']),
                          opens=list(df['open']),
                          highs=list(df['high']),
                          lows=list(df['low']),
                          closes=list(df['close']),
                          weight=.4
                          )
        add_line_series('plot', 'MA', list(df['id']), list(df['mv7']),
                        color=[204, 0, 204])
    start_dearpygui(primary_window='BTC chart')


if __name__ == '__main__':
    run_chart()
    # matplot_chart()
