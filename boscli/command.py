# -*- coding: utf-8 -*-

import six

class Command(object):
	def __init__(self, keywords, command_function = None):
		self.keywords = keywords
		self.command_function = command_function
		
	def _match_word(self, index, token, partial_line):
		definition_for_that_index = self.keywords[index]
		if isinstance(definition_for_that_index, six.string_types):
			return definition_for_that_index == token
		else:
			return definition_for_that_index.match(token, partial_line=partial_line)

	def match(self, tokens):
		for index, word in enumerate(tokens):
			if not self._match_word(index, word, partial_line=tokens):
				return False
		return True

	def matching_parameters(self, tokens):
		assert(self.match(tokens))
		parameters=[]
		for index, token in enumerate(tokens):
			if not isinstance(self.keywords[index], six.string_types):
				parameters.append(token)
		return parameters

	def execute(self, interpreter=None, tokens=None):
		if self.command_function:
			return self.command_function(tokens=tokens, interpreter=interpreter)
