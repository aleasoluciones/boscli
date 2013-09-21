# -*- coding: utf-8 -*-

import unittest
from doublex import *

import boscli
from boscli import exceptions, basic_types
from boscli import parser as parser_module
from boscli import interpreter as interpreter_module


class InterpreterBasicCommandExecutionTest(unittest.TestCase):

    def setUp(self):
        parser = parser_module.Parser()
        self.interpreter = interpreter_module.Interpreter(parser)
        self.cmds_implementation = Spy()
        self._add_command(['cmd', 'key'], self.cmds_implementation.cmd)
        self._add_command(['cmd_with_parameters', basic_types.StringType(), basic_types.StringType()],
                          self.cmds_implementation.cmd_with_parameters)
        self._add_command(['cmd_with_ops', basic_types.OptionsType(['op1', 'op2'])],
                          self.cmds_implementation.cmd_with_ops)


    def _add_command(self, tokens, func):
        self.interpreter.add_command(boscli.Command(tokens, func))

    def test_a_command_match_if_all_the_keywords_match(self):
        self.interpreter.eval('cmd key')

        assert_that(self.cmds_implementation.cmd,
                    called().with_args(tokens=['cmd', 'key'], interpreter=self.interpreter))

    def test_execute_a_command_with_two_parameters(self):
        self.interpreter.eval('cmd_with_parameters param1 param2')

        assert_that(self.cmds_implementation.cmd_with_parameters,
                    called().with_args('param1', 'param2',
                                       tokens=['cmd_with_parameters', 'param1', 'param2'],
                                       interpreter=self.interpreter))

    def test_execute_a_command_with_a_string_parameter(self):
        self.interpreter.eval('cmd_with_parameters param1 "param with spaces"')

        assert_that(self.cmds_implementation.cmd_with_parameters,
                    called().with_args('param1', "param with spaces",
                                       tokens=['cmd_with_parameters', 'param1', "param with spaces"],
                                       interpreter=self.interpreter))

    def test_execute_a_command_with_options_parameters(self):
        self.interpreter.eval('cmd_with_ops op1')

        assert_that(self.cmds_implementation.cmd_with_ops,
                    called().with_args('op1',
                                       tokens=['cmd_with_ops', 'op1'],
                                       interpreter=self.interpreter))

    def test_invalid_option_not_match_for_a_options_parameter(self):
        self.assertRaises(exceptions.NotMatchingCommandFoundError, 
                          self.interpreter.eval, 'cmd_with_ops invalid_op')

    def test_empty_line_evaluation_returns_none(self):
        assert_that(self.interpreter.eval(''), is_(None))


class InterpreterEvaluationErrorsTest(unittest.TestCase):

    def setUp(self):
        parser = parser_module.Parser()
        self.interpreter = interpreter_module.Interpreter(parser)
        self.eth_configurator = Spy()

    def _add_command(self, tokens, func):
        self.interpreter.add_command(boscli.Command(tokens, func))

    def test_exception_raised_when_evaluating_a_line_not_matching_any_command(self):
        self.assertRaises(
            exceptions.NotMatchingCommandFoundError, self.interpreter.eval, "unknown command")

    def test_exception_raised_when_more_than_one_command_match(self):
        self._add_command(['cmd'], Stub().cmd1)
        self._add_command(['cmd'], Stub().cmd2)
        self.assertRaises(exceptions.AmbiguousCommandError, self.interpreter.eval, 'cmd')
