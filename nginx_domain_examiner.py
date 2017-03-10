#!/usr/bin/env python3

import os
import argparse
import re

def get_files_list(confdir="./"):
  flist = []
  for root, subdirs, files in os.walk(confdir):
    for filename in files:
      flist.append(os.path.join(root,filename))
  return flist

# get tuple server_name + domain name
def get_ips(config_file):
  r = re.findall('([0-9]+.[0-9]+.[0-9]+.[0-9]+)', config_file)
  return list(set(r))

def get_server_name(config_file):
  r = re.search('(server_name)\ +(.*\..{2,});', config_file)
  if r:
    return r.groups()
  else:
    return ('none', 'none')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", help="directory containing configs", type=str, default='./')
  parser.add_argument("--domain", help="domain for which print ips", type=str)
  args = parser.parse_args()
  files_list = get_files_list(args.c)

  domains_ips = {}

  for filename in files_list:
    with open(filename, 'r') as f:
      conftxt = f.read()
    srv = get_server_name(conftxt)
    if srv[0] == 'server_name':
      domains_ips[srv[1]] = get_ips(conftxt)
  if args.domain:
    print(domains_ips[args.domain])
  else:
    print(domains_ips)

if __name__ == "__main__":
  main()
