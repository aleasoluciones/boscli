# -*- coding: utf-8 -*-

import unittest
from hamcrest import *
from doublex import *

import boscli
from boscli import parser as parser_module
from boscli import interpreter as interpreter_module
from boscli import completer as completer_module

class AutoCompletionTest(unittest.TestCase):

    def setUp(self):
        parser = parser_module.Parser()
        self.interpreter = interpreter_module.Interpreter(parser)
        self.completer = completer_module.Completer(self.interpreter, parser)
        self.implementation = Stub()

        self.interpreter.add_command(boscli.Command(['sys', 'reboot'], self.implementation.reboot))
        self.interpreter.add_command(boscli.Command(['sys', 'shutdown'], self.implementation.shutdown))
        self.interpreter.add_command(boscli.Command(['net', 'show', 'configuration'], self.implementation.show_net_conf))

    def test_basic_autocompletion(self):
        assert_that(self.completer.complete(''), has_items('sys ', 'net '))
        assert_that(self.completer.complete('sy'), has_items('sys '))
        assert_that(self.completer.complete('sys'), has_items('sys '))
        assert_that(self.completer.complete('sys r'), has_items('reboot '))
        assert_that(self.completer.complete('sys reboot'), has_length(0))
        assert_that(self.completer.complete('unknown command'), has_length(0))
