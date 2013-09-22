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

    def partial_match(self, tokens):
        for index, word in enumerate(tokens):
            if not self._match_word(index, word, partial_line=tokens):
                return False
        return True

    def match(self, tokens, context):
        if self.context_name and self.context_name != context:
            return False
        tokens = self.remove_empty_final_tokens(tokens)
        if len(tokens) != len(self.keywords):
            return False
        return self.partial_match(tokens)

    def exact_match(self, tokens, context):
        return self.match(tokens, context) and self.context_name and self.context_name == context

    def matching_parameters(self, tokens):
        tokens = self.remove_empty_final_tokens(tokens)
        parameters=[]
        for index, token in enumerate(tokens):
            if not isinstance(self.keywords[index], six.string_types):
                parameters.append(token)
        return parameters

    def remove_empty_final_tokens(self, tokens):
        if len(tokens) == 0:
            return tokens
        if tokens[-1] == '':
            tokens = tokens[:-1]
        return tokens

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
