from hamcrest import assert_that, has_items, has_length, contains
from doublex import Stub

from boscli import interpreter as interpreter_module
from boscli import basic_types
from boscli.command import Command

with describe('Autocomplete'):

    with before.each:
        self.interpreter = interpreter_module.Interpreter()
        self.implementation = Stub()

        self.interpreter.add_command(Command(['sys', 'reboot'], self.implementation.reboot))
        self.interpreter.add_command(Command(['sys', 'shutdown'], self.implementation.shutdown))
        self.interpreter.add_command(Command(['net', 'show', 'configuration'], self.implementation.show_net_conf))

    with describe('when autocompleting empty line'):
        with it('complete with initial keywords'):
            assert_that(self.interpreter.complete(''), has_items('sys ', 'net '))

    with describe('when autocompleting keywords'):
        with it('complete keywords'):
            assert_that(self.interpreter.complete('sy'), has_items('sys '))
            assert_that(self.interpreter.complete('sys'), has_items('sys '))
            assert_that(self.interpreter.complete('sys r'), has_items('reboot'))

        with it('not complete when a command match'):
            assert_that(self.interpreter.complete('sys reboot'), has_length(0))
            assert_that(self.interpreter.complete('sys reboot '), has_length(0))

        with it('not complete unknown command'):
            assert_that(self.interpreter.complete('unknown command'), has_length(0))

        with describe('when autocompleting matching and partial matching command'):
            with it('completes partial matching command with space'):
                self.interpreter.add_command(
                    Command(['cmd', CompleteCompletionsType(['op1', 'op2']), 'last'], self.implementation.irrelevant_cmd))
                self.interpreter.add_command(
                    Command(['cmd', CompleteCompletionsType(['op1', 'op2'])], self.implementation.irrelevant_cmd))

                assert_that(self.interpreter.complete('cmd op1'), contains('op1 '))

    with describe('when autocompleting type with completions'):
        with it('completes with the final space if is not the last token'):
            self.interpreter.add_command(Command(['cmd', PlainCompletionsType(['op1', 'op2']), 'last'],
                                         self.implementation.irrelevant_cmd))

            assert_that(self.interpreter.complete('cmd o'), has_items('op1 ', 'op2 '))

        with it('completes without the final space if is the last token'):
            self.interpreter.add_command(Command(['cmd', PlainCompletionsType(['op1', 'op2'])],
                                         self.implementation.irrelevant_cmd))

            assert_that(self.interpreter.complete('cmd o'), has_items('op1', 'op2'))

    with describe('when autocompleting type with complete completions'):
        with it('completes with the final space if is not the last token'):
            self.interpreter.add_command(Command(['cmd', CompleteCompletionsType(['op1', 'op2']), 'last'],
                                         self.implementation.irrelevant_cmd))

            assert_that(self.interpreter.complete('cmd o'), has_items('op1 ', 'op2 '))

        with it('completes without the final space if is the last token'):
            self.interpreter.add_command(Command(['cmd', CompleteCompletionsType(['op1', 'op2'])],
                                         self.implementation.irrelevant_cmd))

            assert_that(self.interpreter.complete('cmd o'), has_items('op1', 'op2'))

    with describe('when autocompleting type with partial completions'):
        with it('completes without the final space if is not the last token'):
            self.interpreter.add_command(Command(['cmd', PartialCompletionsType(['op1', 'op2']), 'last'],
                                         self.implementation.irrelevant_cmd))

            assert_that(self.interpreter.complete('cmd o'), has_items('op1', 'op2'))

    with describe('when autocompleting options type'):
        with it('complete with all matching options'):
            self.interpreter.add_command(Command(['cmd', basic_types.OptionsType(['op1', 'op2'])],
                                    self.implementation.show_net_conf))

            assert_that(self.interpreter.complete('cmd o'), has_items('op1', 'op2'))

    with describe('when autocompleting a string type'):
        with it('no autocomplete at all'):
            self.interpreter.add_command(Command(['cmd', basic_types.StringType()],
                                        self.implementation.show_net_conf))

            assert_that(self.interpreter.complete('cmd '), has_length(0))

    with describe('Filter Autocomplete'):
        with it('autocomplete with space when starting a filter'):
            assert_that(self.interpreter.complete('net show configuration |'), has_items(' '))

        with it('autocomplete all available filters'):
            assert_that(self.interpreter.complete('net show configuration | '), has_items('include'))
            assert_that(self.interpreter.complete('net show configuration | '), has_items('exclude'))

        with it('autocomplete include'):
            assert_that(self.interpreter.complete('net show configuration | inclu'), has_items('include'))

        with it('autocomplete exclude'):
            assert_that(self.interpreter.complete('net show configuration | exclu'), has_items('exclude'))


class _TestCompletionsType(basic_types.BaseType):
    def __init__(self, options):
        self.options = options

    def match(self, word, context, partial_line=None):
        return word in self.options

    def partial_match(self, word, context, partial_line=None):
        for options in self.options:
            if options.startswith(word):
                return True
        return False


class PlainCompletionsType(_TestCompletionsType):
    def complete(self, token, tokens, context):
        return self.options


class CompleteCompletionsType(_TestCompletionsType):
    def complete(self, token, tokens, context):
        return [(value, True) for value in self.options if value.startswith(tokens[-1])]


class PartialCompletionsType(_TestCompletionsType):
    def complete(self, token, tokens, context):
        return [(value, False) for value in self.options if value.startswith(tokens[-1])]
