#!/usr/bin/env python3

import requests
import ast
from datetime import datetime
import sys
import os
from rofi import Rofi
from dearpygui.core import *
from dearpygui.simple import *


# Prayer time calculations
# This program will fetch the prayer time and Hijri date
# from  https://api.aladhan.com/timingsByAddress/
# based on Dubai location.
# On click it will return the day prayers.

name_list = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
rf = Rofi()


def timeformat(tm):
    rm = datetime.strptime(tm , '%H:%M')
    return rm.strftime('%I:%M%p')

def endprogram():
    stop_dearpygui()

def currenttime(tm, dt):
    # check if the prayer is in current time.
    # print(tm)
    ctm = datetime.now()
    newlist = []
    #print('Current Time : ',ctm.strftime('%H:%M'))
    for order in range(len(name_list)):
        if order == len(name_list):
            order = -1
        # print()
        newdict = {}
        current_tm = datetime.strptime(
            tm[name_list[order]] + ' ' + dt, '%H:%M %d-%m-%Y')

        newdict[name_list[order]] = tm[name_list[order]]
        newdict['remainingtime'] = (current_tm - ctm).seconds // 60
        newlist.append(newdict)
        # newdict[prayertime]=tm[name_lis
    # print(newlist)
    seq = [x['remainingtime'] for x in newlist]
    next_time = min(seq)
    next_prayer = min(seq)
    for line in range(len(name_list)):
        if newlist[line]['remainingtime'] == next_time:
            remainingtime = '{:02d}:{:02d}'.format(
                *divmod(newlist[line]['remainingtime'], 60))
            return name_list[line], newlist[line][name_list[line]]


def get_data(all=None):
    para = {'address': 'Dubai,UAE', 'method': '8',
            'tune': '0,6,0,1,0,1,-11,0,0'}
    today = datetime.strftime(datetime.now(), '%d-%m-%Y')

    data = requests.get(
        'https://api.aladhan.com/timingsByAddress/' + today, params=para)
    hdate = requests.get(' http://api.aladhan.com/v1/gToH?date=' + today)

    prtime = ast.literal_eval(data.text)
    prtime = prtime['data']['timings']
    hdate = ast.literal_eval(hdate.text)
    hdate = hdate['data']['hijri']['date']
    ####################
    pname, ptime = currenttime(prtime, today)
    if all is None:
        print(f'{pname} ({ptime}) ({hdate})')
    else:
        prayers = []
        for n in name_list:
            prayers.append((n,prtime[n]))
        return prayers, pname

def runapp(data):
    # print(prayers)
    prayers, pname = data
    today = datetime.now().ctime()
    set_main_window_size(250, 250)
    add_additional_font('/home/sultan/.fonts/Exo-Regular.ttf', 22)
    # set_global_font_scale(1.2)
    set_theme("Grey")
    with window('Prayer Times'):
        add_text(today, color=[6,255,72])
        add_table('Prayer List', ['Prayer', 'Time'], height=180)
        for p in prayers:
            if p[0] == pname:
                add_row('Prayer List',[f'(({p[0]}))', timeformat(p[1])])
            add_row('Prayer List',[p[0], timeformat(p[1])])
        add_button('Quit', callback=endprogram)
    start_dearpygui(primary_window='Prayer Times')

        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        runapp(get_data(all))
        get_data()
    else:
        get_data()
