# -*- coding: utf-8 -*-
import os
import sys
import cherrypy
import threading
import json

from subprocess import check_output

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

from unittest import TestCase
from nose.tools import eq_, ok_
from view import *

V = 'v0.1'

def send_data(path, api_version=V, address='localhost', port=8080, json_file_name=None, errors=None, method='GET'):
	url = address+':'+str(port)+'/'+api_version+'/'+path
	if json_file_name is None:
		output = check_output("http "+method+" "+url, shell=True)
	else:
		output = check_output("http "+method+" "+url+" < "+json_file_name, shell=True)
	return json.loads(output.decode('utf-8'))

class test1(TestCase):
	def setUp(self):
		th = threading.Thread(target=run, kwargs={"host":'localhost', "port":8080, "debug":True, "server":'cherrypy'})
		th.setDaemon(True)
		th.start()
		#th = threading.Thread(target=run, kwargs={"host":'localhost', "port":8080, "debug":True, "server":'cherrypy'})
		#th.setDaemon(True)
		#style = {"style_name": "ACADEMIC", "debater_num_per_team":4, "team_num":2, "score_weights":[1, 1, 1, 1], "replies":[], "num_of_replies":0}
		#t = Tournament(1, "testtournament", 4, style)

	def tearDown(self):
		pass

	def test_create_tournament_callback(self):
		with open('create_tournament_response.json') as data_file:    
			data = json.load(data_file)

		output = send_data('tournaments', json_file_name='create_tournament.json', method='POST')
		eq_(output, data)

	def test_xbit(self):
		pass


