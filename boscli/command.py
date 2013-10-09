# -*- coding: utf-8 -*-

import six

class Command(object):
    def __init__(self, keywords, command_function = None, help=None, context_name=None):
        self.keywords = keywords
        self.command_function = command_function
        self.help = help
        self.context_name = context_name

    def __str__(self):
        return " ".join(str(token_definition) for token_definition in self.keywords)

    def _match_word(self, index, token, partial_line):
        definition_for_that_index = self.keywords[index]
        if self._is_keyword(definition_for_that_index):
            return definition_for_that_index == token
        else:
            return definition_for_that_index.match(token, partial_line=partial_line)

    def _partial_match_last_word(self, index, word, partial_line):
        definition_for_that_index = self.keywords[index]
        if self._is_keyword(definition_for_that_index):
            return definition_for_that_index.startswith(word)
        else:
            return definition_for_that_index.partial_match(word, partial_line=partial_line)

    def partial_match(self, tokens):
        if len(tokens) > len(self.keywords):
            return False

        for index, word in enumerate(tokens):
            if index == len(tokens) -1:
                if not self._partial_match_last_word(index, word, partial_line=tokens):
                    return False
            else:
                if not self._match_word(index, word, partial_line=tokens):
                    return False
        return True

    def context_match(self, context):
        if self.context_name and not context:
            return False
        if self.context_name and context and not context.has_name(self.context_name):
            return False
        return True

    def match(self, tokens, context):
        if not self.context_match(context):
            return False
        if len(tokens) != len(self.keywords):
            return False
        for index, word in enumerate(tokens):
            if not self._match_word(index, word, partial_line=tokens):
                return False
        return True

    def exact_match(self, tokens, context):
        if not self.match(tokens, context):
            return False
        if self.context_name and not context:
            return False
        if  context and not context.has_name(self.context_name):
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
        if self.match(tokens, context):
            return []

        if not len(tokens):
            token_to_complete_index = 0
            token_to_complete = ''
        else:
            token_to_complete_index = len(tokens) -1
            token_to_complete = tokens[-1]

        definition_for_that_index = self.keywords[token_to_complete_index]
        if self._is_keyword(definition_for_that_index):
            if definition_for_that_index == token_to_complete:
                return [token_to_complete + ' ']
            if definition_for_that_index.startswith(token_to_complete):
                return [definition_for_that_index + ' ']
        else:
            return definition_for_that_index.complete(tokens)
        return []

    def _is_keyword(self, definition):
        return isinstance(definition, six.string_types)
