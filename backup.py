#!/usr/bin/env python3

import os
import tarfile
import subprocess
import time
from pathlib import Path
import amazons3
import configparser

# rewrite 
REWRITE = 0
BACKUPCONF = '/opt/backup.ini'
NAMEDATA = '%Y-%m-%d'

def writelog(log, result):
    try:
        with open(log + time.strftime(NAMEDATE) + '.log') as log:
            if result[1] == 1:
                log.write('{}:{}'.format(result[0], 'error')
            if result[1] == 0:
                log.write('{}:{}'.format(result, os.path.getsize(result))
    except Exception as err:
        print(err)


def mysqldump(dbname, dst='./', user='root', password='', host='localhost'):
    if password != '':
        dbpass = '-p' + password
    else:
        dbpass = ''
    dstpath = '{}{}.{}.sql.gz'.format(dst, dbname, time.strftime(NAMEDATE))
    dstfile = Path(dstpath)
    if dstfile.exists() and REWRITE == 0:
        print(dstpath, "exists, won't do")
        return (dstpath, 1)
    print('dumping', dbname)
    mysqlcmd = 'mysqldump --single-transaction --quick -u {} {} -h {} {} | gzip > {}'.format(user, dbpass,\
            host, dbname, dstpath
    res = subprocess.check_output(mysqlcmd, stderr=subprocess.STDOUT, shell=True)
    return (dstpath, 0)

def getmysqldblist(user='root', password='', host='localhost', ignoredb=[]):
    if password != '':
        dbpass = '-p' + password
    else:
        dbpass = ''
    try:
        mysqlcmd = 'mysql -u {} {} -h {} -B -e "show databases"'.format(user, dbpass, host)
        res = subprocess.check_output(mysqlcmd, stderr=subprocess.STDOUT, shell=True)
        dblist = res.decode()
        dblist = dblist.rstrip().lstrip('Database\n')
        dblist = dblist.split('\n')
    except:
        dblist = 'error'
    return dblist


def archiveit(source, target):
    dstfile = Path(target)
    if dstfile.exists() and REWRITE == 0:
        print(target, "exists, won't do")
        return (target, 2)
    print("creating archive:", source)
    try:
        archive = tarfile.open(target, 'w')
        archive.add(source)
        archive.close()
        return (target, 0)
    except Exception as err:
        print('error creating archive')
        return (target, 1)

def main():
    config = configparser.ConfigParser()
    config.read(BACKUPCONF)
    sourcedirs = os.listdir(config['BACKUP']['sourcedir'])
    exclude_str = config['BACKUP']['exclude']
    exclude =  exclude_str.split(',')
    dbexclude_str = config['BACKUP']['dbexclude']
    dbexclude =  dbexclude_str.split(',')

    for excl in exclude:
        try:
            sourcedirs.remove(excl)
        except:
            pass

    s3cli = amazons3.s3client()
    for sdir in sourcedirs:
        archname = '{}{}.{}.tar'.format(config['BACKUP']['storagedir'], sdir, time.strftime(NAMEDATE))
        res = archiveit(config['BACKUP']['sourcedir'] + sdir, archname)
        writelog(config['BACKUP']['logdir'], res)
        if res[1] == 0:
            shortname = '{}.{}.tar'.format(sdir, time.strftime(NAMEDATE))
            s3cli.putobj(shortname, config['BACKUP']['s3bucket'], config['BACKUP']['s3dir'])

    fulldblist = getmysqldblist()
    dblist = [x for x in fulldblist if x not in dbexclude]
    for db in dblist:
        res = mysqldump(db, config['BACKUP']['storagedir'])
        writelog(config['BACKUP']['logdir'], res)
        if res[1] == 0:
            shortname = '{}.{}.sql.gz'.format(sdir, time.strftime(NAMEDATE))
            s3cli.putobj(shortname, config['BACKUP']['s3bucket'], config['BACKUP']['s3dir'])

if __name__ == "__main__":
  main()
