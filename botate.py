#!/usr/bin/env python3

import os
import shutil
from datetime import datetime, timedelta

ROTATEDIR = '/home/vayw/test/'
DAILY = 7
WEEKLY = 8
MONTHLY = 'all'

flist = {}

for f in os.listdir(ROTATEDIR):
    flist[f] = os.path.getmtime(ROTATEDIR + f)
    #flist_sorted = sorted(flist, key = flist.get, reverse)

dailydelta = datetime() - timedelta(days=DAILY)
daily_count = 0


print (flist)
