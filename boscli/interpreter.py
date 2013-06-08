# -*- coding: utf-8 -*-

from boscli import exceptions
from boscli import parser

class Interpreter(object):
	def __init__(self, parser=parser.Parser()):
		self._commands = []
		self.parser = parser

	def add_command(self, command):
		self._commands.append(command)

	def eval(self, line_text):
		if not line_text:
			return

		tokens = self.parser.parse(line_text)
		matching_commands = self._select_matching_commands(tokens)

		if len(matching_commands) == 1:
			return self._execute_command(matching_commands[0], tokens)
		if len(matching_commands) > 0:
			raise exceptions.AmbiguousCommandError(matching_commands)
		raise exceptions.NotMatchingCommandFoundError(line_text)

	def _execute_command(self, command, tokens):
		arguments = command.matching_parameters(tokens)
		return command.execute(*arguments, tokens=tokens, interpreter=self)

	def _select_matching_commands(self, tokens):
		return [command for command in self._commands if command.match(tokens)]

	def active_commands(self):
		return self._commands
