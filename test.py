# -*- coding: utf-8 -*-
import json
from subprocess import *

def send_data(uri, api_version='v0.1', address='localhost', port=8080, json_file_name=None, errors=None, method='GET'):
	url = address+':'+str(port)+'/'+api_version+'/'+uri
	if json_file_name is None:
		output = check_output(["http", method, url])
	else:
		output = check_output(["http", method, url, "<", json_file_name])
	return json.loads(output.decode('utf-8'))

if __name__ == '__main__':
	send_data('tournaments')