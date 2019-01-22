# gunicorn 实践

## 背景

由于项目使用gunicorn部署，随着项目越来越大，需要优化的地方越来越多，所以需要对gunicorn的一些用法需要深度的了解一下，大概涉及一些官方不是很好理解的应用配置。

## 项目环境

+ python 2.7.15
+ gunicorn (latest)19.9.0
+ CentOS 7.6

## git 地址

https://github.com/everpuck/gunicorn_sample.git

## 实践一

---
preload_app 在后台线程中的使用

+ 测试线程

```python
def test_thread(interval=10):
    while True:
        # log.info('time now: %s', time.strftime("%Y-%m-%d %H:%M:%S", time.mktime()))
        print 'time now: %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        time.sleep(interval)
```

+ 测试启动配置一

```python
import multiprocessing

bind = "0.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
reload = True
```

+ 运行命令
> gunicorn -c app_cfg_1 app_1:app

可以看到每个进程都有自己的后台线程输出时间

```text
time now: 2019-01-20 17:05:13
time now: 2019-01-20 17:05:13
time now: 2019-01-20 17:05:13
time now: 2019-01-20 17:05:13
time now: 2019-01-20 17:05:13
time now: 2019-01-20 17:05:13
time now: 2019-01-20 17:05:13
time now: 2019-01-20 17:05:13
time now: 2019-01-20 17:05:13
```

+ 测试启动配置二：加上preload_app选项
> gunicorn -c app_cfg_1 --preload app_1:app

可以看到只有一个线程每隔10秒输出一次时间，验证了该后台线程只在master进程里起了一次。

```text
time now: 2019-01-20 17:08:49
time now: 2019-01-20 17:08:59
time now: 2019-01-20 17:09:09
time now: 2019-01-20 17:09:20
```

## 实践二

---
preload_app 在后台进程中的使用测试

> + 测试结果和线程类似，
> + 但是在worker进程重启的时候报错(设定max_requests的值后)

```text
[2019-01-21 14:21:39 +0000] [7477] [INFO] Autorestarting worker after current request.
[2019-01-21 14:21:39 +0000] [7477] [INFO] Worker exiting (pid: 7477)
Error in atexit._run_exitfuncs:
Traceback (most recent call last):
  File "/usr/local/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
    func(*targs, **kargs)
  File "/usr/local/lib/python2.7/multiprocessing/util.py", line 328, in _exit_function
    p.join()
  File "/usr/local/lib/python2.7/multiprocessing/process.py", line 146, in join
    assert self._parent_pid == os.getpid(), 'can only join a child process'
AssertionError: can only join a child process
Error in sys.exitfunc:
Traceback (most recent call last):
  File "/usr/local/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
    func(*targs, **kargs)
  File "/usr/local/lib/python2.7/multiprocessing/util.py", line 328, in _exit_function
    p.join()
  File "/usr/local/lib/python2.7/multiprocessing/process.py", line 146, in join
    assert self._parent_pid == os.getpid(), 'can only join a child process'
AssertionError: can only join a child process
```

> google后意思是gunicorn在fork进程出现的问题，不推荐这样使用，原帖也给出了迂回解决方法，地址为：https://github.com/benoitc/gunicorn/issues/1391

preload 为True的情况下，会将辅助线程或者进程开在master里，加重master的负担（master最好只是用来负责监听worker进程），以及在内存吃紧的情况下如果做一些占用内存的工作会不会被Linux oom机制杀掉从而使服务挂掉。

## 实践三

---
多进程共享变量

> + python 支持的内存共享变量只有ctype的array 和value
> + 使用multiprocess 下的Manager可是实现多进程共享变量，但是同样遇到实践二里的报错。。。
> + 使用multiprocess 下的**Queue**, 可以实现多进程通信

## 实践四

---
server hooks的使用

### on starting

第一次启动gunicorn前执行
> 只执行一次

### when ready

服务成功启动之后会执行
> 只执行一次

### pre fork

worker进程启动前执行
> worker每次重启都会执行

### post fork

worker进程启动后执行
> 每次worker重启成功后就会执行

### post_worker_init

Called just after a worker has initialized the application.

worker初始化完APP后执行
> worker重启后也会执行

### pre request

每次请求前执行
> 可获取到req的信息，做一些操作，需要注意的是如果正好worker重启则貌似不会执行

### post request

每次请求后执行
> 可获取到req resp的信息，做一些操作，需要注意的是如果正好worker重启则貌似不会执行
