#!/usr/bin/env python3

import time
import os
import shutil
import tarfile
import logging

HOWOLD = 1

basepath = 'E:/1CBufferDirectory/1CUTAxelot'
logging.basicConfig(filename=basepath + '/archivate.log', format='%(levelname)s:%(message)s', level=logging.INFO)

try:
    if os.path.getsize(basepath + '/archivate.log') > 52428800:
        os.remove(basepath + '/archivate.log')
except IOError:
    logging.info('previous log not found')

logging.info('%s | starting..', time.strftime('%d.%m.%Y %H:%M', time.localtime()))
arch_dir = basepath + '/lucky_' + time.strftime('%d_%m_%Y-%H%M%S', time.localtime())
logging.info('creating temporary dir %s..', arch_dir)
os.mkdir(arch_dir)

now = time.time()

logging.info('moving qualified files to temporary dir..')
for i in os.listdir(basepath + '/lucky'):
    cr_time = os.path.getctime(basepath + '/lucky/' + i)
    days_old = (now - cr_time)/60/60/24
    if days_old > HOWOLD:
        logging.debug('moving', i, '..')
        shutil.move(basepath + '/lucky/' + i, arch_dir)

logging.info('compressing directory..')
with tarfile.open(arch_dir + '.tar.bz2', 'w:bz2', compresslevel=9) as tar:
    tar.add(arch_dir)

logging.info('removing temporary dir..')
shutil.rmtree(arch_dir)

logging.info('done at %s', time.strftime('%d.%m.%Y %H:%M', time.localtime()))
