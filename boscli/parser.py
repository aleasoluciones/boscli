# -*- coding: utf-8 -*-

import token, tokenize, StringIO


class Parser(object):

	def parse(self, input_line):
		tokens = []
		rawstr = StringIO.StringIO(input_line)
		for i, item in enumerate(tokenize.generate_tokens(rawstr.readline)):
			_, token_text, (_, _), (_, _), _ = item
			if token_text:
				if token_text.startswith("'") or token_text.startswith('"'):
					token_text = token_text[1:-1]
				tokens.append(token_text)
		return tokens