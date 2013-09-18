# -*- coding: utf-8 -*-

import unittest
from doublex import *

import boscli
from boscli import exceptions
from boscli import parser as parser_module
from boscli import interpreter as interpreter_module


class InterpreterTest(unittest.TestCase):

	def setUp(self):
		parser = parser_module.Parser()
		self.interpreter = interpreter_module.Interpreter(parser)
		self.eth_configurator = Spy()

	def _add_command(self, tokens, func):
		self.interpreter.add_command(boscli.Command(tokens, func))

        def test_exception_raised_when_evaluating_a_line_not_matching_any_command(self):
            self.assertRaises(
                exceptions.NotMatchingCommandFoundError, self.interpreter.eval, "unknown command")

        def test_empty_line_evaluation_returns_none(self):
            assert_that(self.interpreter.eval(''), is_(None))

        def test_exception_raised_when_more_than_one_command_match(self):
            self._add_command(['cmd'], Stub().cmd1)
            self._add_command(['cmd'], Stub().cmd2)
            self.assertRaises(exceptions.AmbiguousCommandError, self.interpreter.eval, 'cmd')

