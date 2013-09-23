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
        self._add_command(['cmd1'], self.context_commands.cmd1, context_name='context1')
        self._add_command(['cmd2'], self.context_commands.cmd2, context_name='context1')
        self._add_command(['exit'], self.context_commands.exit, context_name='context1')

    def _add_command(self, tokens, func, context_name=None):
        self.interpreter.add_command(boscli.Command(tokens, func, context_name=context_name))

    def test_execute_context_commands_with_the_interpreter_at_the_requiered_context(self):
        self.interpreter.push_context('context1')
        self.interpreter.eval('cmd1')
        self.interpreter.eval('cmd2')

        assert_that(self.context_commands.cmd1, called().with_args(ANY_ARG))
        assert_that(self.context_commands.cmd2, called().with_args(ANY_ARG))
        assert_that(self.interpreter.actual_context().has_name('context1'), is_(True))

    def test_no_context_commands_execution_when_the_interpreter_not_at_the_requiered_context(self):
        self.assertRaises(exceptions.NotMatchingCommandFoundError, self.interpreter.eval, "cmd1")
        self.assertRaises(exceptions.NotMatchingCommandFoundError, self.interpreter.eval, "cmd2")

    def test_execute_main_commands_if_not_at_specific_context(self):
        self.interpreter.eval('exit')

        assert_that(self.main_commands.exit, called().with_args(ANY_ARG))

    def test_more_priority_to_the_command_with_the_matching_context(self):
        self.interpreter.push_context('context1')
        self.interpreter.eval('exit')

        assert_that(self.context_commands.exit, called().with_args(ANY_ARG))

    def test_attach_info_to_the_actual_context(self):
        self.interpreter.push_context('context1')
        context_data = self.interpreter.actual_context().data
        context_data['key1'] = 'data1'
        context_data['key2'] = 'data2'

        assert_that(self.interpreter.actual_context().data, is_({'key1':'data1', 'key2':'data2'}))

    def test_context_are_stackables(self):
        self.interpreter.push_context('context1')
        self.interpreter.push_context('context2')
        assert_that(self.interpreter.actual_context().context_name, is_('context2'))
        self.interpreter.pop_context()
        assert_that(self.interpreter.actual_context().context_name, is_('context1'))

    def test_raise_error_when_pop_context_and_no_context_defined(self):
        self.assertRaises(exceptions.NotContextDefinedError, self.interpreter.pop_context)

