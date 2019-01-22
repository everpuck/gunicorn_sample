# coding: utf-8

import os
import time
import threading
import json
from multiprocessing import Manager
from logger import MyLog
from common import updateCurrencyRate
from const import *

curpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
logpath = os.path.join(curpath, "logger")
main_logger = MyLog(loggerName='main', nameTail='main', logPath=logpath, debug=True)
thread_logger = MyLog(loggerName='thread', nameTail='thread', logPath=logpath, debug=True)

manager = Manager()
MCURRENCY_RATES = manager.dict(CURRENCY_RATES)


mthread = threading.Thread(target=updateCurrencyRate,
            args=(CURRENCY_REQ_URL, MCURRENCY_RATES))
mthread.setDaemon(True)
mthread.start()

print MCURRENCY_RATES

def parse_urlargs(urlargs):
    conts = urlargs.split('?')
    args = {}
    if 2 == len(conts):
        params = conts[1].split('&')
        for param in params:
            try:
                items = param.split('=')
                k = items[0]
                v = items[1]
                args[k] = v
            except:
                pass
    return args


def app(environ, start_response):
    """Simplest possible application object"""
    print dir(environ)
    print environ
    
    # if environ['REQUEST_METHOD'].upper() == 'POST':
    #     # ------ 获取并解析请求参数 ------ #
    #     raw_url =  urllib.unquote(environ['RAW_URI'])
    #     try:
    #         remoteAddr = str(environ['REMOTE_ADDR'])
    #     except: pass
    #     url_args = parse_urlargs(raw_url)
        # buf = environ['wsgi.input'].read()
        # data = response.SerializeToString()

    # data = b'Hello, World!\n'
    data = {}
    for key in MCURRENCY_RATES.keys():
        data[key] = MCURRENCY_RATES.get(key)
    data = json.dumps(data)
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)

    return iter([data])
