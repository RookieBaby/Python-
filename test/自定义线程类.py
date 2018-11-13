# -*- coding:utf-8 -*-
import threading,time

class MyThread(threading.Thread):
    def __init__(self,target,arg=()):
        super(MyThread, self).__init__()
        self.target=target
        self.arg=arg

    def run(self):
        self.target(self.arg)

def test(arg):
    time.sleep(1)
    print("current thread is : ",arg)

if __name__ == '__main__':
    for tmp in range(10):
        mt=MyThread(target=test,arg=(tmp,))
        mt.start()
    print("main thread has been stopped")
    