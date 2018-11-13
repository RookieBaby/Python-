# -*- coding:utf-8 -*-

import threading
import time
import uuid

def showThreading(arg):
	time.sleep(1)
	print("current thread is: ", arg)

if __name__ == '__main__':
	for tmp in range(10):
		t = threading.Thread(target=showThreading,args=(tmp,))
		t.start()
	print('main thread has been stopped!')