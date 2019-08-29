# coding: utf-8

import gevent
from gevent import monkey
monkey.patch_all()
import os
# import time
import threading
import json
import requests
# from multiprocessing import Queue
from logger import MyLog
# from common import updateCurrencyRate, test_thread
# from common import test_mem_queue
from const import *

curpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
logpath = os.path.join(curpath, "logger")
main_logger = MyLog(loggerName='main', nameTail='main', logPath=logpath, debug=True)
thread_logger = MyLog(loggerName='thread', nameTail='thread', logPath=logpath, debug=True)

urls = [
    'https://www.baidu.com/',
    'https://www.apple.com/',
    'https://www.python.org/'
]

def print_head(url):
    print 'Starting %s' % url
    data = requests.get(url).text
    print '%s: %s bytes: %r' % (url, len(data), data[:50])


# MEM_QUEUE = Queue()

# mthread = threading.Thread(target=test_mem_queue, args=(MEM_QUEUE,))
# mthread.setDaemon(True)
# mthread.start()


def app(environ, start_response):
    """Simplest possible application object"""
    # if environ['REQUEST_METHOD'].upper() == 'POST':
    #     buf = environ['wsgi.input'].read()
        # MEM_QUEUE.put(buf)

    # for url in urls:
        # print_head(url)
    jobs = [gevent.spawn(print_head, _url) for _url in urls]
    gevent.wait(jobs)

    data = "hello world\n"
    # data = json.dumps(data)
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)

    return iter([data])
