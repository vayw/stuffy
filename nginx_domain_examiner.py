#!/usr/bin/env python3

import os
import argparse
import re
import socket

def get_files_list(confdir="./"):
  flist = []
  for root, subdirs, files in os.walk(confdir):
    for filename in files:
      flist.append(os.path.join(root,filename))
  return flist

def get_ips(config_file):
  ips = []
  for line in config_file.split('\n'):
    if 'listen' in line:
      r = re.search('(listen)\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', line)
      if r:
        ips.append(r.group(2))
  return list(set(ips))

def ip_search(config_file, config_files):
  ips = []
  simple_search = get_ips(config_file)
  if len(simple_search) == 0:
    # let's look for include statement with our config_file in
    # config_files
    for filename in config_files:
      with open(filename, 'r') as f:
        try:
          conftxt = f.read()
        except:
          continue
      server_block_open = False
      include_found = False
      for line in conftxt.split('\n'):
        if re.search('\s*server\s+\{', line):
          server_block_open = True
          continue
        elif config_file in line and server_block_open:
          include_found = True
        elif 'listen' in line:
          if include_found:
            
      

# get tuple server_name + domain name
def get_server_name(config_file):
  r = re.search('(server_name)\ +(.*);', config_file)
  names = r.group(2).split()
  if r:
    return names
  else:
    return None

def check_identity(domain_data, verbose=False):
  if len(domain_data[1]) == 0:
      print(domain_data[0], ":", "listen addresses not specified")
      return
  try:
    dns_result = socket.gethostbyname_ex(domain_data[0])
  except socket.gaierror:
    print(domain_data[0], ':', "failed to resolve!")
    return 0
  except Exception as e:
    print(domain_data)
    print(e)
  dns_ips = set(dns_result[2])
  config_ips = set(domain_data[1])

  if config_ips != dns_ips:
    print(domain_data[0], ':')
    print('dns a-record:', dns_ips)
    print('config listen:', config_ips)
  elif config_ips == dns_ips and verbose:
    print(domain_data[0], ':', 'success')


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", help="directory containing configs", type=str, default='./')
  parser.add_argument("--domain", help="domain for which print ips", type=str)
  parser.add_argument("--test", help="check identity with DNS", action="store_true")
  parser.add_argument("-v", "--verbose", help="increase verbosity", action="store_true")
  args = parser.parse_args()
  files_list = get_files_list(args.c)

  domains_ips = {}

  for filename in files_list:
    with open(filename, 'r') as f:
      try:
        conftxt = f.read()
      except:
        continue

    srv = get_server_name(conftxt)
    if srv not None:
      if len(srv) == 1:
        domains_ips[srv[0]] = get_ips(conftxt)
      elif len(srv) >= 2:
        jips = get_ips(conftxt)
        for i in srv:
          domains_ips[i] = jips

  if len(domains_ips) == 0:
    print("no configuration found!")
    return 0

  if args.domain:
    try:
      print(domains_ips[args.domain])
    except KeyError:
      print(args.domain, "not found!"
  elif args.test is False:
    print(domains_ips)

  if args.test:
    if args.domain:
      check_identity((args.domain, domains_ips[args.domain]), args.verbose)
    else:
      for domain in domains_ips:
        check_identity((domain, domains_ips[domain]), args.verbose)

if __name__ == "__main__":
  main()
