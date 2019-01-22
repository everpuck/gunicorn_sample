# coding: utf-8

import os
import time
# import threading
import json
from multiprocessing import Process, Manager
from logger import MyLog
# from common import updateCurrencyRate, test_thread
# from common import test_thread
from const import *

curpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
logpath = os.path.join(curpath, "logger")
main_logger = MyLog(loggerName='main', nameTail='main', logPath=logpath, debug=True)
thread_logger = MyLog(loggerName='thread', nameTail='thread', logPath=logpath, debug=True)

manager = Manager()
MEM_DICT = manager.dict({
    'name': 'test',
    'value': 'test_value'
})
# MEM_DICT = {}

# mprocess = Process(target=test_thread, args=(10,))
# mprocess.daemon = True
# mprocess.start()


def app(environ, start_response):
    """Simplest possible application object"""
    data = {}
    for key in MEM_DICT.keys():
        data[key] = MEM_DICT.get(key)

    if environ['REQUEST_METHOD'].upper() == 'POST':
        buf = environ['wsgi.input'].read()
        buf = json.loads(buf)
        data.update(buf)

    data = json.dumps(data)
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)

    return iter([data])
