# -*- coding: utf-8 -*-

import six

class Command(object):
    def __init__(self, keywords, command_function = None, help=None, context_name=None, allways=False):
        self.keywords = keywords
        self.command_function = command_function
        self.help = help
        self.context_name = context_name
        self.allways = allways

    def __str__(self):
        return " ".join(str(token_definition) for token_definition in self.keywords)

    def __repr__(self):
        return str(self)

    def normalize_tokens(self, tokens):
        result = []
        for index, word in enumerate(tokens):
            definition_for_that_index = self.keywords[index]
            if self._is_keyword(definition_for_that_index):
                result.append(definition_for_that_index)
            else:
                result.append(word)
        return result

    def _match_word(self, index, word, context, partial_line):
        definition = self.keywords[index]
        if self._is_keyword(definition):
            return definition.startswith(word)
        else:
            return definition.match(word, context, partial_line=partial_line)

    def _partial_match(self, index, word, context, partial_line):
        definition = self.keywords[index]
        if self._is_keyword(definition):
            return definition.startswith(word)
        else:
            return definition.partial_match(word, context, partial_line=partial_line)

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
        if self.allways is True:
            return True
        if self.context_name and not context:
            return False

        if context and context.has_name(self.context_name):
            return True
        if context is None:
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
        if self.normalize_tokens(tokens) != tokens:
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
            if definition == token:
                if self.match(tokens, context):
                    return []
                else:
                    return [token + ' ']
            if definition.startswith(token):
                return [definition + ' ']
        else:
            return definition.complete(tokens, context)
        #return []

    def _select_token_to_complete(self, tokens):
        if not len(tokens):
            return (self.keywords[0], '')
        else:
            return (self.keywords[len(tokens) -1], tokens[-1])
            
    def _is_keyword(self, definition):
        return isinstance(definition, six.string_types)
