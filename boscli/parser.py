# -*- coding: utf-8 -*-

import six
import token, tokenize


class Parser(object):

	def parse(self, input_line):
		tokens = []
		rawstr = six.StringIO(input_line)
		for i, item in enumerate(tokenize.generate_tokens(rawstr.readline)):
			_, token_text, (_, _), (_, _), _ = item
			if token_text:
				if token_text.startswith("'") or token_text.startswith('"'):
					token_text = token_text[1:-1]
				tokens.append(token_text)
		return tokens