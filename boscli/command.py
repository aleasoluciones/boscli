# -*- coding: utf-8 -*-

import six
from boscli import basic_types


class KeywordType(object):
    def __init__(self, name=None):
        self.name = name

    def complete(self, token, tokens, context):
        if self.name.startswith(token):
            return [(self.name, True)]
        return []

    def match(self, word, context, partial_line=None):
        return word == self.name

    def partial_match(self, word, context, partial_line=None):
        if self.name.startswith(word):
            return True
        return False

    def __str__(self):
        return '%s' % self.name


class Command(object):
    def __init__(self, keywords, command_function=None, help=None, context_name=None, always=False, cmd_id=None):
        self.definitions = []
        for definition in keywords:
            if isinstance(definition, six.string_types):
                self.definitions.append(KeywordType(definition))
            else:
                self.definitions.append(definition)

        self.keywords = keywords
        self.command_function = command_function
        self.help = help
        self.context_name = context_name
        self.always = always
        self.cmd_id = cmd_id

    def __lt__(self, other):
        # Dummy sort help function (to avoid problems sorting command
        # sequences using python 3.x
        return self.__str__().__lt__(other.__str__())

    def __str__(self):
        return " ".join(str(token_definition) for token_definition in self.keywords)

    def __repr__(self):
        return str(self)

    def normalize_tokens(self, tokens, context):
        result = []
        for index, word in enumerate(tokens):
            definition_for_that_index = self.keywords[index]
            if self._is_keyword(definition_for_that_index):
                result.append(definition_for_that_index)
            else:
                result.append(self._expand_parameter(self.definitions[index], word, tokens, context))
        return result

    def _match_word(self, index, word, context, partial_line):
        definition = self.definitions[index]
        if isinstance(definition, KeywordType):
            return definition.partial_match(word, context, partial_line=partial_line)
        else:
            word = self._expand_parameter(self.definitions[index], word, partial_line, context)
            return self.definitions[index].match(word, context, partial_line=partial_line)

    def _expand_parameter(self, definition, word, tokens, context):
        completions = definition.complete(word, tokens, context)
        if len(completions) == 1:
            return completions[0][0]
        return word

    def _partial_match(self, index, word, context, partial_line):
        return self.definitions[index].partial_match(word, context, partial_line=partial_line)

    def partial_match(self, tokens, context):
        if len(tokens) > len(self.keywords):
            return False

        for index, word in enumerate(tokens):
            if index == len(tokens) -1:
                if not self._partial_match(index, word, context, partial_line=tokens):
                    return False
            else:
                if not self._match_word(index, word, context, partial_line=tokens):
                    return False

        return True

    def context_match(self, context):
        if self.always is True:
            return True

        if self.context_name and context.is_default():
            return False

        if not self.context_name and context.is_default():
            return True

        if context.has_name(self.context_name):
            return True
        return False

    def match(self, tokens, context):
        if not self.context_match(context):
            return False
        if len(tokens) != len(self.keywords):
            return False
        for index, word in enumerate(tokens):
            if not self._match_word(index, word, context, partial_line=tokens):
                return False
        return True

    def perfect_match(self, tokens, context):
        if not self.match(tokens, context):
            return False
        if self.normalize_tokens(tokens, context) != tokens:
            return False
        return True

    def matching_parameters(self, tokens):
        parameters=[]
        for index, token in enumerate(tokens):
            if not isinstance(self.keywords[index], six.string_types):
                parameters.append(token)
        return parameters

    def execute(self, *args, **kwargs):
        if self.command_function:
            return self.command_function(*args, **kwargs)

    def complete(self, tokens, context):
        definition, token = self._select_token_to_complete(tokens)
        return self.completions(definition, token, tokens, context)

    def completions(self, definition, token, tokens, context):
        if self._is_keyword(definition):
            raw_completions = self._complete_keyword(definition, token, tokens, context)
        else:
            raw_completions = definition.complete(token, tokens, context)

        completions = []
        for completion in raw_completions:
            if isinstance(completion, tuple):
                completions.append(completion[0] + (' ' if completion[1] else ''))
            else:
                completions.append(completion.strip() + ' ')

        return [
            completion.strip() if self._is_last_token(tokens) else completion for completion in completions
        ]

    def _complete_keyword(self, definition, token, tokens, context):
        if definition == token:
            if not self.match(tokens, context):
                return [token]
        elif definition.startswith(token):
            return [definition]

        return []

    def _is_last_token(self, tokens):
        return len(tokens) == len(self.keywords)

    def _select_token_to_complete(self, tokens):
        if not len(tokens):
            return (self.keywords[0], '')
        else:
            return (self.keywords[len(tokens) -1], tokens[-1])

    def _is_keyword(self, definition):
        return isinstance(definition, six.string_types)
