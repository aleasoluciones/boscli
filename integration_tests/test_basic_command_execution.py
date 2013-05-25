import unittest
from doublex import *

import boscli

IRRELEVANT_KEYWORD1 = 'key1'
IRRELEVANT_KEYWORD2 = 'key2'

class BasicCommandExecutionTest(unittest.TestCase):
	def test_execute_command_when_the_corresponding_input_is_evaluated(self):
		commands = Spy()
		interpreter = boscli.Interpreter()

		command1 = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2], commands.command1)
		interpreter.add_command(command1)
		interpreter.eval(IRRELEVANT_KEYWORD1 + ' ' + IRRELEVANT_KEYWORD2)

		assert_that(commands.command1, 
			called().with_args(line=IRRELEVANT_KEYWORD1 + ' ' +  IRRELEVANT_KEYWORD2, 
							   interpreter=interpreter))