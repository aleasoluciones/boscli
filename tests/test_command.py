import unittest
from doublex import *
import boscli

IRRELEVANT_KEYWORD1 = 'irrelevant_keyword1'
IRRELEVANT_KEYWORD2 = 'irrelevant_keyword2'
IRRELEVANT_LINE = 'irrelevant_line'
IRRELEVANT_INTERPRETER = 'irrelevant_interpreter'
IRRELEVANT_RESULT = 'irrelevant_result'

class CommandTest(unittest.TestCase):
	
	def test_a_command_match_if_all_the_keywords_match(self):
		command = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2])
		assert_that(command.match(IRRELEVANT_KEYWORD1 + ' ' + IRRELEVANT_KEYWORD2), is_(True))

	def test_foo(self):
		with Spy() as command_implementation:
			command_implementation.command(ANY_ARG).returns(IRRELEVANT_RESULT)

		command = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2], command_implementation.command)
		command_return_value = command.execute(line=IRRELEVANT_LINE, interpreter=IRRELEVANT_INTERPRETER)

		assert_that(command_implementation.command, called().with_args(line=IRRELEVANT_LINE, interpreter=IRRELEVANT_INTERPRETER))
		assert_that(command_return_value, is_(IRRELEVANT_RESULT))
