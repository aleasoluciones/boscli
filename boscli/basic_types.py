# -*- coding: utf-8 -*-

import re


class BaseType(object):
    def __init__(self, name=None):
        self.name = name

    def complete(self, tokens, context):
        return []

    def match(self, word, context, partial_line=None):
        return False

    def partial_match(self, word, context, partial_line=None):
        return False

    def __str__(self):
        if hasattr(self, 'name') and self.name:
            return '<%s>' % self.name
        return '<%s>' % self.__class__.__name__


class OptionsType(BaseType):

    def __init__(self, valid_options):
        super(OptionsType, self).__init__()
        self.valid_options = valid_options

    def match(self, word, context, partial_line=None):
        return word in self.valid_options

    def partial_match(self, word, context, partial_line=None):
        for op in self.valid_options:
            if op.startswith(word):
                return True
        return False

    def complete(self, tokens, context):
        return [option for option in self.valid_options if option.startswith(tokens[-1])]

    def __str__(self):
        return '<%s>' % ('|'.join(self.valid_options))


class StringType(BaseType):

    def __init__(self, name=None):
        super(StringType, self).__init__(name)

    def match(self, word, context, partial_line=None):
        return True

    def partial_match(self, word, context, partial_line=None):
        return True


class RegexType(BaseType):
    def __init__(self, regex, name=None):
        super(RegexType, self).__init__(name)
        self.regex = re.compile(regex)

    def match(self, word, context, partial_line=None):
        return not self.regex.match(word) is None

    def partial_match(self, word, context, partial_line=None):
        return self.match(word, partial_line)
