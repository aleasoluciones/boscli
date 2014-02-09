# -*- coding: utf-8 -*-

from mamba import *
from hamcrest import *
from doublex import *

import boscli
from boscli import interpreter as interpreter_module
from boscli import basic_types

with describe('Autocomplete') as _:

    @before.each
    def set_up():
        _.interpreter = interpreter_module.Interpreter()
        _.implementation = Stub()

        _.interpreter.add_command(boscli.Command(['sys', 'reboot'], _.implementation.reboot))
        _.interpreter.add_command(boscli.Command(['sys', 'shutdown'], _.implementation.shutdown))
        _.interpreter.add_command(boscli.Command(['net', 'show', 'configuration'], _.implementation.show_net_conf))

    with describe('when autocompleting empty line'):
        def it_complete_with_initial_keywords():
            assert_that(_.interpreter.complete(''), has_items('sys ', 'net '))

    with describe('when autocompleting keywords'):

        def it_complete_keywords():
            assert_that(_.interpreter.complete('sy'), has_items('sys '))
            assert_that(_.interpreter.complete('sys'), has_items('sys '))
            assert_that(_.interpreter.complete('sys r'), has_items('reboot '))

        def it_not_complete_when_a_command_match():
            assert_that(_.interpreter.complete('sys reboot'), has_length(0))
            assert_that(_.interpreter.complete('sys reboot '), has_length(0))

        def it_not_complete_unknown_command():
            assert_that(_.interpreter.complete('unknown command'), has_length(0))

    with describe('when autocompleting options type'):
        def it_complete_with_all_matching_options():
            _.interpreter.add_command(boscli.Command(['cmd', basic_types.OptionsType(['op1', 'op2'])],
                                    _.implementation.show_net_conf))

            assert_that(_.interpreter.complete('cmd o'), has_items('op1', 'op2'))

    with describe('when autocompleting a string type'):
        def it_no_autocomplete_at_all():
            _.interpreter.add_command(boscli.Command(['cmd', basic_types.StringType()],
                                        _.implementation.show_net_conf))

            assert_that(_.interpreter.complete('cmd '), has_length(0))

    with describe('Filter Autocomplete'):
        def it_autocomplete_with_space_when_starting_a_filter():
            assert_that(_.interpreter.complete('net show configuration |'), has_items(' '))

        def it_autocomplete_all_available_filters():
            assert_that(_.interpreter.complete('net show configuration | '), has_items('include'))
            assert_that(_.interpreter.complete('net show configuration | '), has_items('exclude'))

        def it_autocomplete_include():
            assert_that(_.interpreter.complete('net show configuration | inclu'), has_items('include'))

        def it_autocomplete_exclude():
            assert_that(_.interpreter.complete('net show configuration | exclu'), has_items('exclude'))

