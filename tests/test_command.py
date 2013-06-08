# -*- coding: utf-8 -*-

import unittest
from doublex import *
import boscli

IRRELEVANT_KEYWORD1 = 'irrelevant_keyword1'
IRRELEVANT_KEYWORD2 = 'irrelevant_keyword2'
IRRELEVANT_KEYWORD3 = 'irrelevant_keyword3'
IRRELEVANT_LINE = 'irrelevant_line'
IRRELEVANT_INTERPRETER = 'irrelevant_interpreter'
IRRELEVANT_RESULT = 'irrelevant_result'
IRRELEVANT_VALUE = 'irrelevant_value'

class CommandTest(unittest.TestCase):
	
	def test_a_command_match_if_all_the_keywords_match(self):
		command = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2])
		assert_that(command.match([IRRELEVANT_KEYWORD1]), is_(False))
		assert_that(command.match([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2]), is_(True))
		assert_that(command.match([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, IRRELEVANT_KEYWORD3]), is_(False))

	def test_a_command_match_if_all_the_keywords_and_types_match(self):
		line_to_eval = IRRELEVANT_KEYWORD1 + ' ' + IRRELEVANT_KEYWORD2 + ' ' + IRRELEVANT_VALUE
		with Stub() as parameter_type:
			parameter_type.match(IRRELEVANT_VALUE, partial_line=line_to_eval.split()).returns(True)

		command = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, parameter_type])
		assert_that(command.match([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, IRRELEVANT_VALUE]), is_(True))

	def test_execute_a_command_excute_the_configured_implementation(self):
		with Spy() as command_implementation:
			command_implementation.command(ANY_ARG).returns(IRRELEVANT_RESULT)

		command = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2], command_implementation.command)
		command_return_value = command.execute(tokens=[IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2], 
											   interpreter=IRRELEVANT_INTERPRETER)

		assert_that(command_implementation.command, called().with_args(tokens=[IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2], interpreter=IRRELEVANT_INTERPRETER))
		assert_that(command_return_value, is_(IRRELEVANT_RESULT))

	def test_select_matching_parameters_from_tokens_corresponding_to_types(self):
		line_to_eval = IRRELEVANT_KEYWORD1 + ' ' + IRRELEVANT_KEYWORD2 + ' ' + IRRELEVANT_VALUE
		with Stub() as parameter_type:
			parameter_type.match(IRRELEVANT_VALUE, partial_line=line_to_eval.split()).returns(True)

		command = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, parameter_type])
		assert_that(command.matching_parameters([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, IRRELEVANT_VALUE]), 
			is_([IRRELEVANT_VALUE]))

	def test_a_command_partialy_match_if_all_the_given_tokens_match(self):
		command = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2])

		assert_that(command.partial_match([IRRELEVANT_KEYWORD1]), is_(True))
	
	def test_partial_keyword_complete_with_the_rest_of_the_keyword_and_a_space(self):
		command = boscli.Command(['keyword1', 'keyword2'])

		assert_that(command.complete(['key']), is_(['word1 ']))
		assert_that(command.complete(['keyword1', 'key']), is_(['word2 ']))

	def test_complete_all_the_keyword(self):
		command = boscli.Command(['keyword1', 'keyword2'])

		assert_that(command.complete(['keyword1', '']), is_(['keyword2 ']))

	def test_complete_with_a_separator(self):
		command = boscli.Command(['keyword1', 'keyword2'])

		assert_that(command.complete(['keyword1']), is_([' ']))

	def test_when_the_partial_text_dont_match_no_completion_at_all(self):
		command = boscli.Command(['keyword1'])

		assert_that(command.complete(['unknown_keyword']), is_([]))
		
	
	
