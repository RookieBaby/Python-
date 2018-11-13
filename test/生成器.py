# -*- coding:utf-8 -*-

def squares(n):
	i = 1
	while (i <= n):
		yield i**2
		i += 1

if __name__ == '__main__':
	for i in squares(10):
		print(i)
