# -*- coding: utf-8 -*-

import shlex


class Parser(object):

	def parse(self, input_line):
		tokens = shlex.split(input_line)
		if input_line.endswith(' '):
			return tokens + ['']
		return tokens
	