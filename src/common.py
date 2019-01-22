# -*- coding: utf-8 -*-

import time
import urllib2
import logging
import json

log = logging.getLogger("thread")

def test_thread(interval=10):
    while True:
        # log.info('time now: %s', time.strftime("%Y-%m-%d %H:%M:%S", time.mktime()))
        print 'time now: %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        time.sleep(interval)


def test_mem_queue(queue):
    while True:
        # log.info('time now: %s', time.strftime("%Y-%m-%d %H:%M:%S", time.mktime()))
        print 'time now: %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item = queue.get()
        print item
        time.sleep(1)
