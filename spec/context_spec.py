# -*- coding: utf-8 -*-

from mamba import context, before, describe
from doublex import Spy, assert_that, called, ANY_ARG, is_

import boscli
from boscli import exceptions, basic_types
from boscli import interpreter as interpreter_module


with context('Interpreter context') as _:

    @before.each
    def setUp():
        _.interpreter = interpreter_module.Interpreter()
        _.main_commands = Spy()
        _.context_commands = Spy()
        _add_command(['exit'], _.main_commands.exit)
        _add_command(['cmd1'], _.context_commands.cmd1, context_name='context1')
        _add_command(['cmd2'], _.context_commands.cmd2, context_name='context1')
        _add_command(['exit'], _.context_commands.exit, context_name='context1')

    def _add_command(tokens, func, context_name=None):
        _.interpreter.add_command(boscli.Command(tokens, func, context_name=context_name))

    with describe('when not in the required context'):
        def it_execute_main_commands():
            _.interpreter.eval('exit')

            assert_that(_.main_commands.exit, called().with_args(ANY_ARG))

    with describe('when not in any context'):
        def it_not_execute_command_from_other_context():
            try:
                _.interpreter.eval('cmd1')
                _.interpreter.eval('cmd2')
            except exceptions.NotMatchingCommandFoundError:
                pass

        with describe('when pop context'):
            def it_raise_error_because_no_context_defined():
                try:
                    _.interpreter.pop_context()
                except exceptions.NotContextDefinedError:
                    pass

    with describe('when inside a context'):
        def it_executes_commands_from_the_context():
            _.interpreter.push_context('context1')
            _.interpreter.eval('cmd1')
            _.interpreter.eval('cmd2')

            assert_that(_.context_commands.cmd1, called().with_args(ANY_ARG))
            assert_that(_.context_commands.cmd2, called().with_args(ANY_ARG))
            assert_that(_.interpreter.actual_context().has_name('context1'), is_(True))

        def it_executes_commands_from_the_context_not_from_outside():
            _.interpreter.push_context('context1')
            _.interpreter.eval('exit')

            assert_that(_.context_commands.exit, called().with_args(ANY_ARG))

        def it_attach_info_to_the_actual_context():
            _.interpreter.push_context('context1')
            context_data = _.interpreter.actual_context().data
            context_data['key1'] = 'data1'
            context_data['key2'] = 'data2'

            assert_that(_.interpreter.actual_context().data, is_({'key1':'data1', 'key2':'data2'}))

        def it_allow_stack_another_context():
            _.interpreter.push_context('context1')
            _.interpreter.push_context('context2')
            assert_that(_.interpreter.actual_context().context_name, is_('context2'))

            _.interpreter.pop_context()

            assert_that(_.interpreter.actual_context().context_name, is_('context1'))

        def the_default_prompt_is_empty():
            assert_that(_.interpreter.prompt, is_(''))

        def the_default_context_prompt_is_the_context_name():
            _.interpreter.push_context('context1')

            assert_that(_.interpreter.prompt, is_('context1'))

    with describe('when pushing a context with a prompt'):
        def it_assign_the_prompt_to_the_context():
            _.interpreter.push_context('context1', prompt='prompt1')

            assert_that(_.interpreter.prompt, is_('prompt1'))
