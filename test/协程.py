# -*- coding:utf-8 -*-

from gevent import monkey

monkey.patch_all()
import requests,gevent

def fetch_all():
	print('current url is: %s' % url)
	rp = requests.get(url)
	data = rp.text
	print(url, len(data))

if __name__ == '__main__':
	gevent.joinall([
		gevent.spawn(fetch, 'https://www.baidu.com'),
		gevent.spawn(fetch, 'https://www.sogou.com'),
		gevent.spawn(fetch, 'https://www.janshu.com'),
	])