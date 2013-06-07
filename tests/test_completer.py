# -*- coding: utf-8 -*-

import unittest
from doublex import *
from hamcrest import *
import boscli


class Completer(object):
	def __init__(self, interpreter):
		self.interpreter = interpreter
	
	def complete(self, line_to_complete):
		return None


class CompleterTest(unittest.TestCase):

	def test_complete_using_only_the_active_commands_with_partial_match_the_previous_tokens(self):
		command1 = Stub(boscli.Command)
		command2 = Stub(boscli.Command)
		interpreter = Stub(boscli.Interpreter)
		with interpreter:
			interpreter.active_commands().returns([command1, command2])

		with command1:
			command1.partial_match(['keyword1']).returns(True)
			command1.complete(['keyword1', 'partial_keyword2']).returns(['completion1', 'completion2'])

		with command2:
			command2.partial_match(['keyword1']).returns(False)



		completer = Completer(interpreter)

		assert_that(completer.complete('keyword1 partial_keyword2'), has_items('completion1', 'completion2'))
		assert_that(command2.complete, never(called()))
