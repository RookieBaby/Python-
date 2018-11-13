# -*- coding:utf-8 -*-

import threading, time

NUM = 0

def add():
	global NUM
	lock.acquire()
	NUM += 1
	name = t.getName()
	lock.release()
	time.sleep(1)
	print('current thread is: ',name ,' current NUM is: ',NUM )

if __name__ == '__main__':
	lock=threading.Lock()
	for tmp in range(10):
		t = threading.Thread(target=add)
		t.start()
	print("main thread has been stopped !")