import multiprocessing

bind = "0.0.0.0:8888"
cpu_num = multiprocessing.cpu_count()
workers= cpu_num - int(round(cpu_num / 10.0))
proc_name = "gunicorn_sample"
default_proc_name = "gunicorn_sample"
