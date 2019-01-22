# coding: utf-8
"""
    app_cfg_5.py

    Created by everpuck on 2019/01/22
    Copyright (c) 2019 elong. All rights reserved
"""


import multiprocessing

bind = "127.0.0.1:8000"
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 2
# preload_app = True
max_requests = 2


# Called just before the master process is initialized.
def on_starting(server):
    print 'on start'
    print multiprocessing.cpu_count() * 2 + 1


# Called just after the server is started.
def when_ready(server):
    print "Server is ready. Spawning workers"


def pre_fork(server, worker):
    print 'pre fork'


def post_fork(server, worker):
    print dir(worker)
    print 'post fork'


def post_worker_init(worker):
    print 'post_worker_init'


# Called just after a worker exited on SIGINT or SIGQUIT.
# def worker_int(worker):
#     print 'worker int'

# Called just before a new master process is forked.
# def pre_exec(server):
#     print 'pre exec'


# Called just before a worker processes the request.
def pre_request(worker, req):
    print "%s %s" % (req.method, req.path)


# Called after a worker processes the request.
def post_request(worker, req, environ, resp):
    print "%s %s" % (req.method, req.path)
    print "%s %s" % (environ, resp)
    print dir(resp)
