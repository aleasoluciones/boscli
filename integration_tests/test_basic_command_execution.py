# -*- coding: utf-8 -*-

import unittest
from doublex import *

import boscli
from boscli import basic_types

IRRELEVANT_KEYWORD1 = 'key1'
IRRELEVANT_KEYWORD2 = 'key2'
IRRELEVANT_OP1_WITH_SPACES = 'op 1'
IRRELEVANT_OP2 = 'op2'

class BasicCommandExecutionTest(unittest.TestCase):

	def test_execute_command_when_the_corresponding_input_is_evaluated(self):
		commands = Spy()
		interpreter = boscli.Interpreter()

		command1 = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2], commands.command1)
		interpreter.add_command(command1)
		interpreter.eval(IRRELEVANT_KEYWORD1 + ' ' + IRRELEVANT_KEYWORD2)

		assert_that(commands.command1, 
			called().with_args(tokens=[IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2], 
							   interpreter=interpreter))

	def test_execute_command_with_option_type(self):
		commands = Spy()
		interpreter = boscli.Interpreter()

		option_type = basic_types.OptionsType([IRRELEVANT_OP1_WITH_SPACES, IRRELEVANT_OP2])
		command1 = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, option_type], commands.command1)
		interpreter.add_command(command1)
		
		line = IRRELEVANT_KEYWORD1 + ' ' + IRRELEVANT_KEYWORD2 + ' ' + '"' + IRRELEVANT_OP1_WITH_SPACES + '"'
		interpreter.eval(line)

		assert_that(commands.command1, 
					called().with_args(IRRELEVANT_OP1_WITH_SPACES, 
									   tokens=[IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, IRRELEVANT_OP1_WITH_SPACES],
		 							   interpreter=interpreter))


