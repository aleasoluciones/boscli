# -*- coding: utf-8 -*-

import six

class Command(object):
	def __init__(self, keywords, command_function = None):
		self.keywords = keywords
		self.command_function = command_function
		
	def _match_word(self, index, word, partial_line):
		definition_for_that_index = self.keywords[index]
		if isinstance(definition_for_that_index, six.string_types):
			return definition_for_that_index == word
		else:
			return definition_for_that_index.match(word, partial_line=partial_line)

	def match(self, line):
		for index, word in enumerate(line.split()):
			if not self._match_word(index, word, partial_line=line.split()):
				return False
		return True

	def execute(self, interpreter=None, line=None):
		if self.command_function:
			return self.command_function(line=line, interpreter=interpreter)
