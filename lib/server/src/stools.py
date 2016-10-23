# -*- coding: utf-8 -*-
import json
from bottle import HTTPResponse, route
from threading import Lock, Thread
import copy

def lock_with(default_lock=None):#does not call the same function at the same time
	def _lock(func):
		"""usage
		@lock(None) # <= if multiple functions want to share the lock, put the lock on this argument.
		def say_hello():
			print("hello")
			time.sleep(1)
		"""
		if default_lock is None:
			closure_lock = Lock()
		else:
			closure_lock = default_lock
		def locked_func(*args, **kwargs):
		    with closure_lock:
		        return func(*args, **kwargs)

		return locked_func
	return _lock

def set_error(status, status_text, message):
	return {"status": status, "status_text": status_text, "message": message}

def lock(func):#does not call the same function at the same time
	"""usage
	@lock_wrapper
	def say_hello():
		print("hello")
		time.sleep(1)
	"""
	closure_lock = Lock()
	def locked_func(*args, **kwargs):
	    with closure_lock:
	        return func(*args, **kwargs)

	return locked_func

def replace_resource_url(resource_url, kwargs):
	resource_url_rev = copy.copy(resource_url)
	resource_url_rev = resource_url_rev.replace('<', '')
	resource_url_rev = resource_url_rev.replace('>', '')
	resource_url_rev = resource_url_rev.replace(':int', '')
	resource_url_rev = resource_url_rev.replace(':float', '')
	resource_url_rev = resource_url_rev.replace(':path', '')
	resource_url_rev = resource_url_rev.replace(':re', '')
	for k, v in kwargs.items():
		resource_url_rev = resource_url_rev.replace(k, str(v))
	return resource_url_rev

def make_json(resource_url):
	def _make_json(func):
		def _(*args, **kwargs):
			retvals = func(*args, **kwargs)
			resource_url_rev = replace_resource_url(resource_url, kwargs)

			if len(retvals) == 2:
				return set_json_response(data=retvals[0], errors=retvals[1], resource_url=resource_url_rev)
			elif len(retvals) == 1:
				return set_json_response(data=null, errors=[set_error(1, 'feature not available', 'wait till its impletmented')], resource_url=resource_url_rev)
		return _
	return _make_json

def set_json_response(data={}, status=200, errors=[], resource_url=""):
	if not data:
		data = None
	body_json = {"errors":errors, "data":data, "resource_url":resource_url}
	body = json.dumps(body_json)
	r = HTTPResponse(status = status, body = body)
	r.set_header('Content-Type', 'application/json')
	return r

def route_json(url, method='GET'):
	def _(func):
		@route(url, method=method)
		@make_json(url)
		def _2(*args, **kwargs):
			return func(*args, **kwargs)
		return _2
	return _

if __name__ == '__main__':
	import time
	lock = Lock()
	@lock_with(lock)
	def test(a):
		print(a)

	t3 = Thread(target=test, args=[1])
	t4 = Thread(target=test, args=[2])
	t5 = Thread(target=test, args=[3])
	t6 = Thread(target=test, args=[4])
	t3.start()
	t4.start()
	t5.start()
	t6.start()
	test(5)