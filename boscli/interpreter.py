# -*- coding: utf-8 -*-

from boscli import exceptions
from boscli import parser

class Context(object):
    def __init__(self, context_name):
        self.context_name = context_name
        self.data = {}

    def has_name(self, context_name):
        return self.context_name == context_name

    def __str__(self):
        return "Context%s"%self.context_name

class Interpreter(object):
    def __init__(self, parser=parser.Parser()):
        self._commands = []
        self.parser = parser
        self.context = []

    def add_command(self, command):
        self._commands.append(command)

    def push_context(self, context_name):
        self.context.append(Context(context_name))

    def pop_context(self):
        try:
            self.context.pop()
        except IndexError:
            raise exceptions.NotContextDefinedError()

    def eval(self, line_text):
        if not line_text:
            return

        tokens = self.parser.parse(line_text)
        matching_commands = self._select_matching_commands(tokens)
        if len(matching_commands) == 1:
            return self._execute_command(matching_commands[0], tokens)
        if len(matching_commands) > 0:
            perfects_matchs = self._select_exact_matching_commands(tokens)
            if len(perfects_matchs) == 1:
                return self._execute_command(perfects_matchs[0], tokens)
            raise exceptions.AmbiguousCommandError(matching_commands)
        raise exceptions.NotMatchingCommandFoundError(line_text)

    def _execute_command(self, command, tokens):
        arguments = command.matching_parameters(tokens)
        return command.execute(*arguments, tokens=tokens, interpreter=self)

    def _select_exact_matching_commands(self, tokens):
        return [command for command in self._commands if command.exact_match(tokens, self.actual_context())]

    def _select_matching_commands(self, tokens):
        return [command for command in self._commands if command.match(tokens, self.actual_context())]

    def actual_context(self):
        if len(self.context) > 0:
            return self.context[-1]
        return None

    def active_commands(self):
        return self._commands

    def partial_match(self, line_text):
        tokens = self.parser.parse(line_text)
        previous_tokens = tokens[:-1]
        return [command for command in self.active_commands() if command.partial_match(previous_tokens)]

    def help(self, line_text):
        result = {}
        for command in self.partial_match(line_text):
            result[command] = command.help
        return result
