# -*- coding: utf-8 -*-

import unittest
from hamcrest import *
from doublex import *

import boscli
from boscli import parser as parser_module
from boscli import interpreter as interpreter_module
from boscli import basic_types

class AutoCompletionTest(unittest.TestCase):

    def setUp(self):
        parser = parser_module.Parser()
        self.interpreter = interpreter_module.Interpreter(parser)
        self.implementation = Stub()

        self.interpreter.add_command(boscli.Command(['sys', 'reboot'], self.implementation.reboot))
        self.interpreter.add_command(boscli.Command(['sys', 'shutdown'], self.implementation.shutdown))
        self.interpreter.add_command(boscli.Command(['net', 'show', 'configuration'], self.implementation.show_net_conf))

    def test_basic_autocompletion(self):
        assert_that(self.interpreter.complete(''), has_items('sys ', 'net '))
        assert_that(self.interpreter.complete('sy'), has_items('sys '))
        assert_that(self.interpreter.complete('sys'), has_items('sys '))
        assert_that(self.interpreter.complete('sys r'), has_items('reboot '))
        assert_that(self.interpreter.complete('sys reboot'), has_length(0))
        assert_that(self.interpreter.complete('sys reboot '), has_length(0))
        assert_that(self.interpreter.complete('unknown command'), has_length(0))

    def test_options_autocompletion(self):
        self.interpreter.add_command(boscli.Command(['cmd', basic_types.OptionsType(['op1', 'op2'])],
            self.implementation.show_net_conf))

        assert_that(self.interpreter.complete('cmd o'), has_items('op1', 'op2'))

    def test_basic_types_has_no_completions(self):
        self.interpreter.add_command(boscli.Command(['cmd', basic_types.StringType()],
            self.implementation.show_net_conf))

        assert_that(self.interpreter.complete('cmd '), has_length(0))