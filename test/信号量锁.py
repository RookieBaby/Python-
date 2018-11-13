# -*- coding:utf-8 -*-
import threading, time


def test():
    semaphore.acquire()
    print("current thread is: ", t.getName())
    time.sleep(1)
    semaphore.release()

if __name__ == '__main__':
    semaphore = threading.BoundedSemaphore(5)
    for tmp in range(20):
        t = threading.Thread(target=test)
        t.start()
    print('main thread has been stopped!')