# -*- coding: utf-8 -*-

import shlex


class Parser(object):

	def parse(self, input_line):
		return shlex.split(input_line)
	