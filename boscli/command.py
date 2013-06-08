# -*- coding: utf-8 -*-

import six

class Command(object):
	def __init__(self, keywords, command_function = None):
		self.keywords = keywords
		self.command_function = command_function
		

	def _match_word(self, index, token, partial_line):
		definition_for_that_index = self.keywords[index]
		if self._is_keyword(definition_for_that_index):
			return definition_for_that_index == token
		else:
			return definition_for_that_index.match(token, partial_line=partial_line)

	def partial_match(self, tokens):
		for index, word in enumerate(tokens):
			if not self._match_word(index, word, partial_line=tokens):
				return False
		return True

	def match(self, tokens):
		if len(tokens) != len(self.keywords):
			return False
		return self.partial_match(tokens)

	def matching_parameters(self, tokens):
		assert(self.match(tokens))
		parameters=[]
		for index, token in enumerate(tokens):
			if not isinstance(self.keywords[index], six.string_types):
				parameters.append(token)
		return parameters

	def execute(self, *args, **kwargs):
		if self.command_function:
			return self.command_function(*args, **kwargs)

	def complete(self, tokens):
		token_to_complete_index = len(tokens) -1
		token_to_complete = tokens[-1]
		definition_for_that_index = self.keywords[token_to_complete_index]
		if self._is_keyword(definition_for_that_index):
			if definition_for_that_index.startswith(token_to_complete):
				return [definition_for_that_index[len(token_to_complete):] + ' ']
		return []

	def _is_keyword(self, definition):
		return isinstance(definition, six.string_types)