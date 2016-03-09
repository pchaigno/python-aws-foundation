#!/usr/bin/env python2
# -*- coding : utf8 -*-

import unittest
from section_four import *

class TestSectionFour(unittest.TestCase):
	def test_init(self):
		self.assertIsNotNone(init_ec2())

	def test_sg(self):
		#[{u'GroupName': 'toto42', u'GroupId': 'sg-xxxxx'}]
		for key,val in list_all_sg():
				self.assertTrue('GroupName' in key)
		

if __name__== '__main__':
	unittest.main()