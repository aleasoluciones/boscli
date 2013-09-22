# -*- coding: utf-8 -*-

class Completer(object):
    def __init__(self, interpreter, parser):
        self.interpreter = interpreter
        self.parser = parser

    def complete(self, line_to_complete):
        completions = set()
        tokens = self.parser.parse(line_to_complete)
        for command in self.interpreter.partial_match(line_to_complete):
            completions.update(command.complete(tokens, self.interpreter.actual_context()))
        return completions
