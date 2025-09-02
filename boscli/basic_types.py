import re


class BaseType:
    def __init__(self, name=None):
        self.name = name

    def complete(self, token, tokens, context):
        return []

    def match(self, word, context, partial_line=None):
        return False

    def partial_match(self, word, context, partial_line=None):
        return False

    def __str__(self):
        if hasattr(self, 'name') and self.name:
            return '<%s>' % self.name
        return '<%s>' % self.__class__.__name__

class OrType:
    def __init__(self, *types, **kwargs):
        self.types = types
        self.name = kwargs.get('name', None)

    def complete(self, token, tokens, context):
        completions = []
        for t in self.types:
            completions.extend(t.complete(token, tokens, context))
        return completions

    def match(self, word, context, partial_line=None):
        for t in self.types:
            if t.match(word, context, partial_line):
                return True
        return False

    def partial_match(self, word, context, partial_line=None):
        for t in self.types:
            if t.partial_match(word, context, partial_line):
                return True
        return False

    def __str__(self):
        if hasattr(self, 'name') and self.name:
            return '<%s>' % self.name
        return '<%s>' % self.__class__.__name__



class OptionsType(BaseType):
    def __init__(self, valid_options=None, name=None):
        super().__init__()
        self.name = name
        self.valid_options = valid_options or []

    def match(self, word, context, partial_line=None):
        return word in self.get_valid_options()

    def partial_match(self, word, context, partial_line=None):
        for op in self.get_valid_options():
            if op.startswith(word):
                return True
        return False

    def complete(self, token, tokens, context):
        return [(option, True)
                for option in self.get_valid_options()
                if option.startswith(token)]

    def get_valid_options(self):
        return self.valid_options

    def __str__(self):
        if self.name is not None:
            return '<%s>' % self.name
        return '<%s>' % ('|'.join(self.get_valid_options()))

class DynamicOptionsType(OptionsType):
    def __init__(self, valid_options_func, name=None):
        self.name = name
        self.valid_options_func = valid_options_func

    def get_valid_options(self):
        return self.valid_options_func()


class StringType(BaseType):

    def __init__(self, name=None):
        super().__init__(name)

    def match(self, word, context, partial_line=None):
        return len(word) > 0

    def partial_match(self, word, context, partial_line=None):
        return len(word) > 0

class BoolType(OptionsType):

    def __init__(self, name=None):
        super().__init__(['true', 'false'], name)


class IntegerType(BaseType):

    def __init__(self, min=None, max=None, name=None):
        super().__init__(name)
        self.min = min
        self.max = max

    def match(self, word, context, partial_line=None):
        try:
            if self.min is not None:
                if int(word) <= self.min:
                    return False
            if self.max is not None:
                if int(word) >= self.max:
                    return False
            return True
        except ValueError:
            return False
    def partial_match(self, word, context, partial_line=None):
        return self.match(word, context, partial_line)


class RegexType(BaseType):
    def __init__(self, regex, name=None):
        super().__init__(name)
        self.regex = re.compile(regex)

    def match(self, word, context, partial_line=None):
        return self.regex.match(word) is not None

    def partial_match(self, word, context, partial_line=None):
        return self.match(word, context, partial_line)
