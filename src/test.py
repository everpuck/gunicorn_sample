# coding:utf-8


import json
from multiprocessing import Process, Value, Array

def f(n, a):
    # n.value = 3.1415927
    n.value = 's'
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('u', u'd')
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print num.value
    print arr[:]