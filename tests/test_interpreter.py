import unittest
from doublex import *

import boscli
from boscli import exceptions

# Initial tests:
# Eval empty line
# Eval line matching a command

IRRELEVANT_LINE = 'irrelevant_line'

class InterpreterTest(unittest.TestCase):

	def test_exception_raised_when_evaluating_a_line_not_matching_any_command(self):
		interpreter = boscli.Interpreter()
	
		self.assertRaises(exceptions.NotMatchingCommandFound, interpreter.eval, IRRELEVANT_LINE)

	def test_execute_the_command_when_match_found(self):
		interpreter = boscli.Interpreter()

		with Spy() as command:
			command.match(IRRELEVANT_LINE).returns(True)
		interpreter.add_command(command)
			
		interpreter.eval(IRRELEVANT_LINE)
		
		assert_that(command.execute, called())
