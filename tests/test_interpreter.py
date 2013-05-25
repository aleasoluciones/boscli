import unittest

import boscli
from boscli import exceptions

# Initial tests:
# Eval empty line
# Eval line not matching any command
# Eval line matching a command

IRRELEVANT_LINE = 'irrelevant_line'

class InterpreterTest(unittest.TestCase):
	def test_exception_raised_when_evaluating_a_line_not_matching_any_command(self):

		interpreter = boscli.Interpreter()
		self.assertRaises(exceptions.NotMatchingCommandFound, interpreter.eval, IRRELEVANT_LINE)