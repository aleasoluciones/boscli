# -*- coding: utf-8 -*-

import unittest
from doublex import *
from hamcrest import all_of, contains_string
import boscli
from boscli import basic_types

IRRELEVANT_KEYWORD1 = 'irrelevant_keyword1'
IRRELEVANT_KEYWORD2 = 'irrelevant_keyword2'
IRRELEVANT_KEYWORD3 = 'irrelevant_keyword3'
IRRELEVANT_LINE = 'irrelevant_line'
IRRELEVANT_INTERPRETER = 'irrelevant_interpreter'
IRRELEVANT_RESULT = 'irrelevant_result'
IRRELEVANT_VALUE = 'irrelevant_value'

IRRELEVANT_COMPLETION1 = 'irrelevant_completion1'
IRRELEVANT_COMPLETION2 = 'irrelevant_completion2'


class CommandTest(unittest.TestCase):

    def test_a_command_match_if_all_the_keywords_match(self):
        command = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2])
        assert_that(command.match([IRRELEVANT_KEYWORD1]), is_(False))
        assert_that(command.match([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2]), is_(True))
        assert_that(command.match([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, '']), is_(True))
        assert_that(command.match([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, IRRELEVANT_KEYWORD3]), is_(False))

    def test_a_command_match_if_all_the_keywords_and_types_match(self):
        line_to_eval = IRRELEVANT_KEYWORD1 + ' ' + IRRELEVANT_KEYWORD2 + ' ' + IRRELEVANT_VALUE
        with Stub(basic_types.BaseType) as type_definition:
            type_definition.match(IRRELEVANT_VALUE, partial_line=line_to_eval.split()).returns(True)

        command = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, type_definition])
        assert_that(command.match([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, IRRELEVANT_VALUE]), is_(True))

    def test_the_empty_line_never_match(self):
        command = boscli.Command(['keyword1', 'keyword2'])
        assert_that(command.match([]), is_(False))

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
        with Stub(basic_types.BaseType) as type_definition:
            type_definition.match(IRRELEVANT_VALUE, partial_line=line_to_eval.split()).returns(True)

        command = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, type_definition])
        assert_that(command.matching_parameters([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, IRRELEVANT_VALUE]),
                is_([IRRELEVANT_VALUE]))
        assert_that(command.matching_parameters([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2, IRRELEVANT_VALUE, '']),
                is_([IRRELEVANT_VALUE]))


    def test_a_command_partialy_match_if_all_the_given_tokens_match(self):
        command = boscli.Command([IRRELEVANT_KEYWORD1, IRRELEVANT_KEYWORD2])

        assert_that(command.partial_match([IRRELEVANT_KEYWORD1]), is_(True))

    def test_partial_keyword_complete_with_the_rest_of_the_keyword_and_a_space(self):
        command = boscli.Command(['keyword1', 'keyword2'])

        assert_that(command.complete(['key']), is_(['keyword1 ']))
        assert_that(command.complete(['keyword1', 'key']), is_(['keyword2 ']))

    def test_complete_all_the_keyword(self):
        command = boscli.Command(['keyword1', 'keyword2'])

        assert_that(command.complete(['keyword1', '']), is_(['keyword2 ']))

    def test_complete_with_a_separator(self):
        command = boscli.Command(['keyword1', 'keyword2'])

        assert_that(command.complete(['keyword1']), is_(['keyword1 ']))

    def test_when_the_partial_text_dont_match_no_completion_at_all(self):
        command = boscli.Command(['keyword1'])

        assert_that(command.complete(['unknown_keyword']), is_([]))

    def test_use_the_var_type_to_complete(self):
        with Stub(basic_types.BaseType) as type_definition:
            type_definition.complete([IRRELEVANT_KEYWORD1, '']).returns([IRRELEVANT_COMPLETION1, IRRELEVANT_COMPLETION2])

        command = boscli.Command([IRRELEVANT_KEYWORD1, type_definition])

        assert_that(command.complete([IRRELEVANT_KEYWORD1, '']),
                is_([IRRELEVANT_COMPLETION1, IRRELEVANT_COMPLETION2]))

    def test_no_completion_generated_when_tokens_match(self):
        command = boscli.Command(['keyword1', 'keyword2'])

        assert_that(command.complete(['keyword1', 'keyword2']), is_([]))

    def test_complete_the_the_empty_line(self):
        command = boscli.Command(['keyword1', 'keyword2'])

        assert_that(command.complete([]), is_(['keyword1 ']))

    def test_command_to_string(self):
        assert_that(str(boscli.Command(['keyword1', 'keyword2'])),
                all_of(contains_string('keyword1'),
                        contains_string('keyword2')))

    def test_by_default_a_command_has_no_help(self):
        command = boscli.Command(['keyword1'])

        assert_that(command.help, is_(None))

    def test_command_help(self):
        command = boscli.Command(['keyword1'], help='irrelevant_help')

        assert_that(command.help, is_('irrelevant_help'))
