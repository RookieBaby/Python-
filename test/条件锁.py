# -*- coding:utf-8 -*-
import threading


def condition():
    inp = input("input your condition: ")
    print(inp)
    if inp == "yes":
        return True
    return False


def test():
    cd.acquire()
    # cd.wait(1)
    cd.wait_for(condition)
    # cd.notify(2)
    print(t.getName())
    cd.release()

if __name__ == '__main__':
    cd = threading.Condition()
    for tmp in range(10):
        t = threading.Thread(target=test)
        t.start()
        t.join()
    print("\nmain thread has been stopped")
