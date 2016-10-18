# -*- coding: utf-8 -*-
import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

from unittest import TestCase
from nose.tools import eq_
from system.modules.bit_modules import *

class testbits(TestCase):
	#def setUp(self):
	#	pass

	#def tearDown(self):
	#	pass

	def test_lastbit(self):
		lb = lastbit(int('1111', 2))
		eq_(lb, 1)

	def test_xbit(self):
		eq_(xbit(int('1101', 2), 1), 0)