# -*- coding: utf-8 -*-
import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

from unittest import TestCase
from nose.tools import eq_, ok_
from system.modules.classes import *

class test1(TestCase):
	def setUp(self):
		style = {"style_name": "ACADEMIC", "debater_num_per_team":4, "team_num":2, "score_weights":[1, 1, 1, 1], "replies":[], "num_of_replies":0}
		t = Tournament(1, "testtournament", 4, style)

	def tearDown(self):
		pass

	def test_lastbit(self):
		pass

	def test_xbit(self):
		pass