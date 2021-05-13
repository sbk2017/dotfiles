#! /usr/bin/env python3

import re
from rofi import Rofi
import os

rf = Rofi()
home = os.environ['HOME']

configfile = home + "/.config/i3/config"


with open(configfile, 'r') as cf:
     lines = cf.readlines()

c = re.compile(r'^bindsym\sMod4\+([A-z0-9\+]*)\s([A-z\s]*)')
keylist = []
#for line in lines :
#     re.findall(c, line))

for line in lines:
     group = re.findall(c, line)
     if len(group) > 0 :
         keylist.append(f'{group[0][0]} : {group[0][1]}')


rf.select(prompt='binding keys', options=keylist)


