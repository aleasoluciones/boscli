# -*- coding: utf-8 -*-

from mamba import describe, before, context
from doublex import Spy
from hamcrest import assert_that, has_entries, contains_string, is_not

import boscli
from boscli import basic_types
from boscli import interpreter as interpreter_module


with describe('Help') as _:

    @before.each
    def set_up():
        _.interpreter = interpreter_module.Interpreter()
        _.command_implementation = Spy()
        _.cmd1 = boscli.Command(['cmd', 'key1'], _.command_implementation.cmd1, help='help_cmd1')
        _.cmd_context = boscli.Command(['cmd', 'key2'], _.command_implementation.netmask, context_name='irrelevant_context', help='help_cmd_context')
        _.cmd_no_help = boscli.Command(['description', basic_types.StringType()], _.command_implementation.description)

        _.interpreter.add_command(_.cmd1)
        _.interpreter.add_command(_.cmd_context)
        _.interpreter.add_command(_.cmd_no_help)

    with context('when asking for help with empty line'):

        with describe('when not in a context'):
            def it_returns_help_for_all_active_commands_that_not_requires_a_context():
                result = _.interpreter.help('')
                assert_that(result, has_entries(_.cmd1, contains_string('help_cmd1'), _.cmd_no_help, None))
                assert_that(result, is_not(has_entries(_.cmd_context, contains_string('help_cmd_context'))))

        with describe('when inside a context'):
            def it_returns_help_for_all_active_commands_including_commands_from_the_actual_context():
                _.interpreter.push_context('irrelevant_context')

                result = _.interpreter.help('')
                assert_that(result, has_entries(_.cmd1, contains_string('help_cmd1'),
                                                _.cmd_context, contains_string('help_cmd_context'),
                                                _.cmd_no_help, None))

    with context('when asking for help with a line with a partial command'):
        def it_returns_help_for_partial_matching_commands():
            result = _.interpreter.help('cmd ')
            assert_that(result, has_entries(_.cmd1, contains_string('help_cmd1')))
            assert_that(result, is_not(has_entries(_.cmd_no_help, None)))
            assert_that(result, is_not(has_entries(_.cmd_context, contains_string('help_cmd_context'))))
