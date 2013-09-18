# -*- coding: utf-8 -*-



class BaseType(object):

    def complete(self, tokens):
        raise NotImplementedError()

    def match(self, word, partial_line=None):
        raise NotImplementedError()


class OptionsType(BaseType):

    def __init__(self, valid_options):
        self.valid_options = valid_options

    def match(self, word, partial_line=None):
        return word in self.valid_options

class StringType(BaseType):

    def __init__(self):
        pass

    def match(self, word, partial_line=None):
        return True
