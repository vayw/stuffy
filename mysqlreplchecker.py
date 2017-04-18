#!/usr/bin/env python3

import subprocess
from slackwebhook import slackWebHook
import time

User = ''
Password = ''
CMD = 'show slave status \G;'
slack_url = ''
ok_gap = 10
sleep_sec = 600

def get_rep_status(user='', passwd='', cmd='show slave status\G;'):
  ppaswd = "-p" + passwd
  raw_output = subprocess.check_output(["mysql", "-u", user, ppaswd, "-e", cmd],\
    stderr=subprocess.DEVNULL)
  output_list = raw_output.decode().split()
  params_list = ['Slave_IO_Running:', 'Seconds_Behind_Master:']
  params = {}
  for i in params_list:
    n = output_list.index(i)
    params[i] = output_list[n+1]
  
  return params

def main():
  print('starting replication monitoring...')
  slack = slackWebHook(slack_url)
  RepState = 0
  RepGap = 0

  while True:
    params = get_rep_status(user=User, passwd=Password, cmd=CMD)
    if params['Slave_IO_Running:'] != 'Yes':
      slack.send('Attention! Replication is not running!')
      RepState = 1
    elif params['Slave_IO_Running:'] == 'Yes' and RepState == 1:
      RepState = 0
      slack.send('Replication recovered!')

    if params['Seconds_Behind_Master:'] != 'NULL':
      sec = int(params['Seconds_Behind_Master:'])
      if sec > ok_gap:
        if sec > RepGap:
          slack.send('Replication is falling back! ' + sec + ' second behind')
        else:
          slack.send('Attention! Slave is ' + sec + ' second behind')
        RepGap = sec
      elif sec < ok_gap and ok_gap < RepGap:
        slack.send('We catch up!')
        RepGap = sec
      elif sec == 0 and RepGap > 0:
        RepGap = 0
        slack.send('Replication is good! Lag is 0')

    time.sleep(sleep_sec)


if __name__ == "__main__":
  main()
