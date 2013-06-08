# -*- coding: utf-8 -*-

import unittest
from doublex import *
from hamcrest import *

import boscli
from boscli import exceptions
from boscli import parser

IRRELEVANT_KEY = 'irrelevant_key'
IRRELEVANT_LINE = 'irrelevant_line'
IRRELEVANT_RESULT = 'irrelevant_result'
IRRELEVANT_VALUE1 = 'irrelevant_value1'
IRRELEVANT_VALUE2 = 'irrelevant_value2'
IRRELEVANT_TOKEN_LIST = ['k1', 'k2']
IRRELEVANT_COMMAND1 = 'irrelevant_command1'
IRRELEVANT_COMMAND2 = 'irrelevant_command2'


class InterpreterTest(unittest.TestCase):

    def setUp(self):
        self.parser = Spy(parser.Parser)
        self.interpreter = boscli.Interpreter(self.parser)

    def test_exception_raised_when_evaluating_a_line_not_matching_any_command(self):
        self.assertRaises(
            exceptions.NotMatchingCommandFoundError, self.interpreter.eval, IRRELEVANT_LINE)

    def test_empty_line_evaluation_returns_none(self):
        assert_that(self.interpreter.eval(''), is_(None))

    def test_exception_raised_when_more_than_one_command_match(self):
        with Spy(boscli.Command) as command1:
            command1.match(ANY_ARG).returns(True)
            command1.matching_parameters(ANY_ARG).returns([])
        with Spy(boscli.Command) as command2:
            command2.match(ANY_ARG).returns(True)
            command2.matching_parameters(ANY_ARG).returns([])

        self.interpreter.add_command(command1)
        self.interpreter.add_command(command2)

        self.assertRaises(
            exceptions.AmbiguousCommandError, self.interpreter.eval, IRRELEVANT_KEY)

    def test_execute_the_command_when_match_found(self):
        with self.parser:
            self.parser.parse(IRRELEVANT_LINE).returns(IRRELEVANT_TOKEN_LIST)

        with Spy(boscli.Command) as command:
            command.match(IRRELEVANT_TOKEN_LIST).returns(True)
            command.matching_parameters(ANY_ARG).returns([])
            command.execute(ANY_ARG).returns(IRRELEVANT_RESULT)

        self.interpreter.add_command(command)

        command_return_value = self.interpreter.eval(IRRELEVANT_LINE)

        assert_that(command.execute, called().with_args(
            tokens=IRRELEVANT_TOKEN_LIST, interpreter=self.interpreter))
        assert_that(command_return_value, is_(IRRELEVANT_RESULT))

    def test_active_commands(self):
        self.interpreter.add_command(IRRELEVANT_COMMAND1)
        self.interpreter.add_command(IRRELEVANT_COMMAND2)

        assert_that(self.interpreter.active_commands(),
                    contains_inanyorder(IRRELEVANT_COMMAND1, IRRELEVANT_COMMAND2))

