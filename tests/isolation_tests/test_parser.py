# -*- coding: utf-8 -*-

import unittest
from doublex import *

from boscli import parser

IRRELEVANT_KEYWORD1 = 'irrelevant_keyword1'
IRRELVANT_KEYWORD2 = 'irrelevant_keyword2'

class ParserTest(unittest.TestCase):

    def test_parse_keywords_separated_by_whitespaces(self):
        assert_that(parser.Parser().parse(IRRELEVANT_KEYWORD1 + ' ' + IRRELVANT_KEYWORD2),
                is_([IRRELEVANT_KEYWORD1, IRRELVANT_KEYWORD2]))

    def test_a_string_as_a_uniq_token(self):
        assert_that(parser.Parser().parse("'python string'"), is_(['python string']))
        assert_that(parser.Parser().parse('"python string"'), is_(['python string']))

    def test_final_separator_parse_as_aditional_empty_token(self):
        assert_that(parser.Parser().parse(IRRELEVANT_KEYWORD1 + ' '), is_([IRRELEVANT_KEYWORD1, '']))
