# -*- coding: utf-8 -*-

from doublex import Spy, assert_that, called, ANY_ARG, is_, when, never

from boscli import exceptions, basic_types
from boscli import interpreter as interpreter_module
from boscli.command import Command

with context('Interpreter context'):

    with before.each:
        self.interpreter = interpreter_module.Interpreter(prompt='irrelevant_prompt')
        self.always_present = Spy()
        self.main_commands = Spy()
        self.context_commands = Spy()
        self._add_command(['exit'], self.main_commands.exit)
        self._add_command(['always_present'], self.always_present.always_present, always=True)
        self._add_command(['cmd1'], self.context_commands.cmd1, context_name='context1')
        self._add_command(['cmd2'], self.context_commands.cmd2, context_name='context1')
        self._add_command(['exit'], self.context_commands.exit, context_name='context1')


    def _add_command(self, tokens, func, context_name=None, always=False):
        self.interpreter.add_command(Command(tokens, func, context_name=context_name, always=always))

    with describe('when not in the required context'):
        with it('not execute main command'):
            try:
                self.interpreter.push_context('context1')
                self.interpreter.eval('exit')
            except exceptions.NoMatchingCommandFoundError:
                pass
            assert_that(self.main_commands.exit, never(called()))


        with it('execute always present commands'):
            self.interpreter.push_context('context1')
            self.interpreter.eval('always_present')

            assert_that(self.always_present.always_present, called().with_args(ANY_ARG))

    with describe('when not in any context'):
        with it('not execute command from other context'):
            try:
                self.interpreter.eval('cmd1')
                self.interpreter.eval('cmd2')
            except exceptions.NoMatchingCommandFoundError:
                pass
            assert_that(self.context_commands.cmd1, never(called()))
            assert_that(self.context_commands.cmd2, never(called()))

        with describe('when pop context'):
            with it('raise error because no context defined'):
                try:
                    self.interpreter.pop_context()
                    raise "Should raise exception"
                except exceptions.NotContextDefinedError:
                    pass

    with describe('when inside a context'):
        with it('executes commands from the context'):
            self.interpreter.push_context('context1')
            self.interpreter.eval('cmd1')
            self.interpreter.eval('cmd2')

            assert_that(self.context_commands.cmd1, called().with_args(ANY_ARG))
            assert_that(self.context_commands.cmd2, called().with_args(ANY_ARG))
            assert_that(self.interpreter.actual_context().has_name('context1'), is_(True))

        with it('executes commands from the context not from outside'):
            self.interpreter.push_context('context1')
            self.interpreter.eval('exit')

            assert_that(self.context_commands.exit, called().with_args(ANY_ARG))

        with it('attach info to the actual context'):
            self.interpreter.push_context('context1')
            context_data = self.interpreter.actual_context().data
            context_data['key1'] = 'data1'
            context_data['key2'] = 'data2'

            assert_that(self.interpreter.actual_context().data, is_({'key1':'data1', 'key2':'data2'}))

        with it('allow stack another context'):
            self.interpreter.push_context('context1')
            self.interpreter.push_context('context2')
            assert_that(self.interpreter.actual_context().context_name, is_('context2'))

            self.interpreter.pop_context()

            assert_that(self.interpreter.actual_context().context_name, is_('context1'))

        with it('the default prompt is interpreter initial prompt'):
            assert_that(self.interpreter.prompt, is_('irrelevant_prompt'))

        with it('the default context prompt is the context name'):
            self.interpreter.push_context('context1')

            assert_that(self.interpreter.prompt, is_('context1'))

    with describe('when pushing a context with a prompt'):
        with it('assign the prompt to the context'):
            self.interpreter.push_context('context1', prompt='prompt1')

            assert_that(self.interpreter.prompt, is_('prompt1'))



with context('Types can use context'):

    with before.each:
        self.interpreter = interpreter_module.Interpreter(prompt='irrelevant_prompt')
        self.type = Spy(basic_types.BaseType)
        self.command = Spy()
        self.interpreter.add_command(Command([self.type], self.command.command, context_name='context1'))

        self.interpreter.push_context('context1', prompt='prompt1')
        self.actual_context = self.interpreter.actual_context()

        when(self.type).complete(ANY_ARG).returns([])
        when(self.type).partial_match(ANY_ARG).returns(True)

    with describe('when autocompleting command'):
        with it('pass context to the type'):
            when(self.type).match(ANY_ARG).returns(False)

            self.interpreter.complete('test')

            assert_that(self.type.partial_match, called().with_args('test', self.actual_context, partial_line=['test']))
            assert_that(self.type.complete, called().with_args('test', ['test'], self.actual_context))

    with describe('when executing command'):
        with it('pass context to the type (to verify if match)'):
            when(self.type).match(ANY_ARG).returns(True)

            self.interpreter.eval('test')

            assert_that(self.type.match, called().with_args('test', self.actual_context, partial_line=['test']))
