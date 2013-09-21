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
        self.eth_configurator = Spy()
        self.ip_address_cmd = boscli.Command(['ip', 'address', basic_types.StringType()], self.eth_configurator.ip_address, help='set address')
        self.netmask_cmd = boscli.Command(['ip', 'netmask', basic_types.StringType()], self.eth_configurator.netmask, help='set netmask')
        self.description_cmd = boscli.Command(['description', basic_types.StringType()], self.eth_configurator.description)

        self.interpreter.add_command(self.ip_address_cmd)
        self.interpreter.add_command(self.netmask_cmd)
        self.interpreter.add_command(self.description_cmd)


    def test_help_for_emptyline_returns_help_for_all_active_commands(self):
        result = self.interpreter.help('')
        assert_that(result,
            has_entries(self.ip_address_cmd, contains_string('address'),
                        self.netmask_cmd, contains_string('netmask'),
                        self.description_cmd, None))

    def test_help_for_line_ontly_returns_help_for_partial_matching_commands(self):
        result = self.interpreter.help('ip ')
        assert_that(result,
            has_entries(self.ip_address_cmd, contains_string('address'),
                        self.netmask_cmd, contains_string('netmask')))
        assert_that(result, is_not(has_entries(self.description_cmd, None)))
