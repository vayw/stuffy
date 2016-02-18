#!/usr/bin/env python3

import os
import datetime

def isweekly(uboundary, bboundary, modtime):
  file_inaccurate_date = datetime.datetime.fromtimestamp(modtime)
  file_inaccurate_date = file_inaccurate_date.replace(minute=0, hour=0, second=0, microsecond=0)
  while 

backup_dir = "/home/vayw/prog/test"
daily = 7
weekly = 8
monthly = 0
# how to determine creation time
# time - by mtime attribute
# name - by file name
determine_type = "time"

# type of backups
# d - directories
# f - any type of files
backups = 'f'

# go to backup directory
os.chdir(backup_dir)
# prepare list of backup files
backups_list = os.listdir()
files_and_mtimes = {}
# prepare deltas
# for daily
daily = datetime.datetime.now() - datetime.timedelta(days=daily)
# for weekly
weekly = daily - datetime.timedelta(weeks=weekly)

for bkpfile in backups_list:
  mtime = os.path.getmtime(bkpfile)
  # lookup for daily 
  if datetime.datetime.now() > datetime.datetime.fromtimestamp(mtime) > daily:
    print("daily:", bkpfile)
    backup_list.pop(bkpfile)
  # lookup for weekly
  elif daily > 

