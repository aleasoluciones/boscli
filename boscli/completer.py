# -*- coding: utf-8 -*-

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
