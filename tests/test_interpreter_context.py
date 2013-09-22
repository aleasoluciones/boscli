# -*- coding: utf-8 -*-

import unittest
from doublex import *

import boscli
from boscli import exceptions, basic_types
from boscli import parser as parser_module
from boscli import interpreter as interpreter_module


class InterpreterContextTest(unittest.TestCase):
    def setUp(self):
        parser = parser_module.Parser()
        self.interpreter = interpreter_module.Interpreter(parser)
        self.main_commands = Spy()
        self.context_commands = Spy()
        self._add_command(['exit'], self.main_commands.exit)
        self._add_command(['cmd1'], self.context_commands.cmd1, context='context1')
        self._add_command(['cmd2'], self.context_commands.cmd2, context='context1')
        self._add_command(['exit'], self.context_commands.exit, context='context1')

    def _add_command(self, tokens, func, context=None):
        self.interpreter.add_command(boscli.Command(tokens, func, context=context))

    def test_execute_context_commands_with_the_interpreter_at_the_requiered_context(self):
        self.interpreter.push_context('context1')
        self.interpreter.eval('cmd1')
        self.interpreter.eval('cmd2')

        assert_that(self.context_commands.cmd1, called().with_args(ANY_ARG))
        assert_that(self.context_commands.cmd2, called().with_args(ANY_ARG))

    def test_no_context_commands_execution_when_the_interpreter_not_at_the_requiered_context(self):
        self.assertRaises(exceptions.NotMatchingCommandFoundError, self.interpreter.eval, "cmd1")
        self.assertRaises(exceptions.NotMatchingCommandFoundError, self.interpreter.eval, "cmd2")
