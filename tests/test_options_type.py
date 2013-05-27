# -*- coding: utf-8 -*-

import unittest
from doublex import *

from boscli import basic_types

IRRELEVANT_OP1 = 'op1'
IRRELEVANT_OP2 = 'op2'

class OptionsTypeTest(unittest.TestCase):
	
	def test_match_only_the_given_options(self):
		options_type = basic_types.OptionsType([IRRELEVANT_OP1, IRRELEVANT_OP2])
		assert_that(options_type.match(IRRELEVANT_OP1), is_(True))
		assert_that(options_type.match(IRRELEVANT_OP2), is_(True))
		assert_that(options_type.match('incorrect_option'), is_(False))