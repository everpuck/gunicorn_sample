# coding=utf-8
"""
    logger.py

    Created by everpuck on 2019/01/22
    Copyright (c) 2019 elong. All rights reserved
"""

import logging
import os
from datetime import datetime
from threading import RLock

MAX_LOG_FILE = 10
MAX_LOG_NUM = 1000000

# log section
if os.name == 'nt':
    DEFAULT_LOG_PATH = 'C:\\dalog'
else:
    DEFAULT_LOG_PATH = '/tmp/dalog'

def createDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

class MyLog(object):

    formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s %(message)s')

    def __init__(self, loggerName='root.vpslog', nameTail=None, logPath=None, debug=False, textHeader=''):
        self.nameTail = nameTail if nameTail else datetime.now().strftime('%Y%m%d-%H%M%S')

        # create log directory
        self.logPath = logPath if logPath else DEFAULT_LOG_PATH
        createDir(self.logPath)

        self.logCount = 0
        self.logFileCount = 0

        # pin log file name
        logFile = self.logPath+os.sep+'log-'+self.nameTail+'-%s'%self.logFileCount

        # get logger by loggerName, set level
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.DEBUG)

        # set file handler
        self.filHandler = logging.FileHandler(logFile)
        self.filHandler.setFormatter(MyLog.formatter)
        self.logger.addHandler(self.filHandler)

        if debug:
            # set show handler
            self.strHandler = logging.StreamHandler()
            self.strHandler.setFormatter(MyLog.formatter)
            self.logger.addHandler(self.strHandler)
        else:
            self.strHandler = None

        # set per row log, begin show info
        self.textHeader = textHeader

        # locker
        self.lock = RLock()

    def addHeader(self, subheader):
        self.textHeader += ' {0} '.format(subheader)

    # log function
    def record(self, text, logFunc=None):
        with self.lock:
            if logFunc:
                logFunc(self.textHeader+" "+text)
                self.checkUpdateHandler()

    def info(self, text):
        self.record(text, self.logger.info)

    def debug(self, text):
        self.record(text, self.logger.debug)

    def warning(self, text):
        self.record(text, self.logger.warning)

    def error(self, text):
        self.record(text, self.logger.error)

    def critical(self, text):
        self.record(text, self.logger.critical)

    def exception(self, text):
        self.record(text, self.logger.exception)

    def checkUpdateHandler(self):
        self.logCount += 1
        if self.logCount >= MAX_LOG_NUM:
            self.logFileCount += 1
            if self.logFileCount >= MAX_LOG_FILE:
                self.logFileCount = 0
            if self.filHandler:
                self.logger.removeHandler(self.filHandler)
            logFile = self.logPath+os.sep+'log-'+self.nameTail+'-%s'%self.logFileCount
            if os.path.isfile(logFile):
                os.remove(logFile)
            self.filHandler= logging.FileHandler(logFile)
            self.filHandler.setFormatter(MyLog.formatter)
            self.logger.addHandler(self.filHandler)
            self.logCount = 0

    # 将日志flush到对应的目标域上，一般在系统退出的时候调用
    def shutdown(self):
        logging.shutdown()
        if self.filHandler:
            self.logger.removeHandler(self.filHandler)

if __name__ == '__main__':
    # loggerName 是日志名称，不同的日志名称会分别记录
    # nameTail 是日志文件名的后缀，便于区分不同的日志文件
    # logPath 是日志文件的存储路径
    # debug 如果是True，除了记录在文件还会打印到屏幕上
    curpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    logpath = os.path.join(curpath, "mainLog")
    logger = MyLog(loggerName='test1', nameTail='test', logPath=logpath, debug=True, textHeader="header")
    logger.info('this is a info test')
    logger.error('this is a error test')
    logger.warning('this is a warning test')
    log = logging.getLogger("test1")
    log.info('hhhhh')

    logger.shutdown()
