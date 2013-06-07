# -*- coding: utf-8 -*-

import unittest
from doublex import *
from hamcrest import *
import boscli
from boscli import parser as parser_module


class Completer(object):
	def __init__(self, interpreter, parser):
		self.interpreter = interpreter
		self.parser = parser
	
	def complete(self, line_to_complete):
		completions = set()
		tokens = self.parser.parse(line_to_complete)
		previous_tokens = tokens[:-1]
		for command in self.interpreter.active_commands():
			if command.partial_match(previous_tokens):
				completions.update(command.complete(tokens))
		return completions


class CompleterTest(unittest.TestCase):

	def test_complete_using_only_the_active_commands_with_partial_match_the_previous_tokens(self):
		with Spy(parser_module.Parser) as parser:
			parser.parse('keyword1 partial_keyword2').returns(['keyword1', 'partial_keyword2'])
		
		with Stub(boscli.Command) as command1:
			command1.partial_match(['keyword1']).returns(True)
			command1.complete(['keyword1', 'partial_keyword2']).returns(['completion1', 'completion2'])

		with Spy(boscli.Command) as command2:
			command2.partial_match(['keyword1']).returns(False)
		
		interpreter = Stub(boscli.Interpreter)
		with interpreter:
			interpreter.active_commands().returns([command1, command2])

		completer = Completer(interpreter, parser)
		result = completer.complete('keyword1 partial_keyword2')

		assert_that(result, has_items('completion1', 'completion2'))
		assert_that(command2.complete, never(called()))
		assert_that(parser.parse, called())
