# -*- coding:utf-8 -*-
from multiprocessing import Process


def test(pro):
    print("current process is: ",pro)


if __name__ == '__main__':
    for tmp in range(10):
        p = Process(target=test,args=(tmp,))
        p.start()
        