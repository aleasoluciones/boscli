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

    def _add_command(self, tokens, func):
        self.interpreter.add_command(boscli.Command(tokens, func))

    def test_exit_raises_end_of_program(self):
        self._add_command(['exit'], lambda *args, **kwargs: self.interpreter.exit())
        self.assertRaises(exceptions.EndOfProgram, self.interpreter.eval, 'exit')
