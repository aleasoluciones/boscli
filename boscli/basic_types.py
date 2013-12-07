# -*- coding: utf-8 -*-

import re


class BaseType(object):

    def complete(self, tokens):
        return []

    def match(self, word, partial_line=None):
        return False

    def partial_match(self, word, partial_line=None):
        return False



class OptionsType(BaseType):

    def __init__(self, valid_options):
        self.valid_options = valid_options

    def match(self, word, partial_line=None):
        return word in self.valid_options

    def partial_match(self, word, partial_line=None):
        for op in self.valid_options:
            if op.startswith(word):
                return True
        return False

    def complete(self, tokens):
        return [option for option in self.valid_options if option.startswith(tokens[-1])]


class StringType(BaseType):

    def __init__(self):
        pass

    def match(self, word, partial_line=None):
        return True

    def partial_match(self, word, partial_line=None):
        return True

class RegexType(BaseType):
    def __init__(self, regex):
        self.regex = re.compile(regex)

    def match(self, word, partial_line=None):
        return not self.regex.match(word) is None

    def partial_match(self, word, partial_line=None):
        return self.partial_match(word, partial_line)