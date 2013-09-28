# -*- coding: utf-8 -*-

import unittest
from doublex import *
from hamcrest import *

import boscli
from boscli import basic_types
from boscli import parser as parser_module
from boscli import interpreter as interpreter_module


class InterpreterHelpTest(unittest.TestCase):

    def setUp(self):
        parser = parser_module.Parser()
        self.interpreter = interpreter_module.Interpreter(parser)
        self.command_implementation = Spy()
        self.cmd1 = boscli.Command(['cmd', 'key1'], self.command_implementation.cmd1, help='help_cmd1')
        self.cmd2 = boscli.Command(['cmd', 'key2'], self.command_implementation.netmask, help='help_cmd2')
        self.cmd_no_help = boscli.Command(['description', basic_types.StringType()], self.command_implementation.description)

        self.interpreter.add_command(self.cmd1)
        self.interpreter.add_command(self.cmd2)
        self.interpreter.add_command(self.cmd_no_help)


    def test_help_for_emptyline_returns_help_for_all_active_commands(self):
        result = self.interpreter.help('')
        assert_that(result,
            has_entries(self.cmd1, contains_string('help_cmd1'),
                        self.cmd2, contains_string('help_cmd2'),
                        self.cmd_no_help, None))

    def test_help_for_line_ontly_returns_help_for_partial_matching_commands(self):
        result = self.interpreter.help('cmd ')
        assert_that(result,
            has_entries(self.cmd1, contains_string('help_cmd1'),
                        self.cmd2, contains_string('help_cmd2')))
        assert_that(result, is_not(has_entries(self.cmd_no_help, None)))
