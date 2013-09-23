# -*- coding: utf-8 -*-



class BaseType(object):

    def complete(self, tokens):
        return []

    def match(self, word, partial_line=None):
        raise NotImplementedError()


class OptionsType(BaseType):

    def __init__(self, valid_options):
        self.valid_options = valid_options

    def match(self, word, partial_line=None):
        return word in self.valid_options

    def complete(self, tokens):
        return [option for option in self.valid_options if option.startswith(tokens[-1])]


class StringType(BaseType):

    def __init__(self):
        pass

    def match(self, word, partial_line=None):
        return True
