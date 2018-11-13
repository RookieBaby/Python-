# -*- coding:utf-8 -*-

A0 = dict(zip(('a','b','c','d','e'), (1,2,3,4,5)))
print(A0)

A1 = [A0[s] for s in A0]
print(A1)
for s in A0:
	print(s)

# 深拷贝和浅拷贝
import copy
a = 1
b = copy.deepcopy(a)
print(id(a), id(b))
a= 2
print(2)
print(id(a), id(b))

c = 3
d = copy.copy(c)
print(id(c),id(d))