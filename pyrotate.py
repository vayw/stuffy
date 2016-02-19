#!/usr/bin/env python3

from sys import exit as sexit
import sys
import datetime

backup_dir = ""
daily = 7
weekly = 8
monthly = 0 # only infinite monthly backups implemented
# all backups which enters in "weekly" interval
# will be checked for day of creation, if this day is one
# of specified below, backup will be keept, otherwise - deleted
weekly_days = [1,7,14,21]
# similar to above statement
mothly_day = 1
# how to determine creation time
# time - by mtime attribute
determine_type = "time"

# type of backups
# d - directories
# f - any type of files
backups = 'f'

def remove(fpath):
  if os.path.isfile(fpath):
    os.remove(fpath)
  elif os.path.isdir(fpath):
    os.rmdir(fpath)

# perform checks
# denied paths
denied = ["", "/", "/home"]
if backup_dir in denied:
  print("this path is denied!")
  sexit(1)

# go to backup directory
os.chdir(backup_dir)
# prepare list of backup files
backups_list = os.listdir()
files_and_mtimes = {}
# prepare deltas
# for daily
daily = datetime.datetime.now() - datetime.timedelta(days=daily + 1)
# for weekly
weekly = daily - datetime.timedelta(weeks=weekly + 1)

for bkpfile in backups_list:
  mtime_stamp = os.path.getmtime(bkpfile)
  mtime = datetime.datetime.fromtimestamp(mtime_stamp)
  # lookup for daily 
  if datetime.datetime.now() > mtime > daily:
    #print("daily:", bkpfile)
    pass
  # lookup for weekly
  elif daily > mtime > weekly and mtime.day in weekly_days:
    #print("weekly:", bkpfile)
    pass
  elif mtime.day == mothly_day:
      #print("monthly:", bkpfile)
      pass
  else:
    remove(bkpfile)
