# coding: utf-8

import os
import time
# import threading
import json
from multiprocessing import Process
from logger import MyLog
# from common import updateCurrencyRate, test_thread
from common import test_thread
from const import *

curpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
logpath = os.path.join(curpath, "logger")
main_logger = MyLog(loggerName='main', nameTail='main', logPath=logpath, debug=True)
thread_logger = MyLog(loggerName='thread', nameTail='thread', logPath=logpath, debug=True)

# manager = Manager()
# MCURRENCY_RATES = manager.dict(CURRENCY_RATES)


mprocess = Process(target=test_thread, args=(10,))
mprocess.daemon = True
mprocess.start()


def app(environ, start_response):
    """Simplest possible application object"""
    # print dir(environ)
    # print environ

    data = b'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)

    return iter([data])
