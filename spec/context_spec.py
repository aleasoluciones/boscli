# -*- coding: utf-8 -*-

from doublex import Spy, assert_that, called, ANY_ARG, is_, when, never

from boscli import exceptions, basic_types
from boscli import interpreter as interpreter_module
from boscli.command import Command

with context('Interpreter context'):

    with before.each:
        self.interpreter = interpreter_module.Interpreter(prompt='irrelevant_prompt')
        self.allways_present = Spy()
        self.main_commands = Spy()
        self.context_commands = Spy()
        self._add_command(['exit'], self.main_commands.exit)
        self._add_command(['allways_present'], self.allways_present.allways_present, allways=True)
        self._add_command(['cmd1'], self.context_commands.cmd1, context_name='context1')
        self._add_command(['cmd2'], self.context_commands.cmd2, context_name='context1')
        self._add_command(['exit'], self.context_commands.exit, context_name='context1')


    def _add_command(self, tokens, func, context_name=None, allways=False):
        self.interpreter.add_command(Command(tokens, func, context_name=context_name, allways=allways))

    with describe('when not in the required context'):
        with it('not execute main command'):
            try:
                self.interpreter.push_context('context1')
                self.interpreter.eval('exit')
            except exceptions.NotMatchingCommandFoundError:
                pass
            assert_that(self.main_commands.exit, never(called()))


        with it('execute allways present commands'):
            self.interpreter.push_context('context1')
            self.interpreter.eval('allways_present')

            assert_that(self.allways_present.allways_present, called().with_args(ANY_ARG))

    with describe('when not in any context'):
        with it('not execute command from other context'):
            try:
                self.interpreter.eval('cmd1')
                self.interpreter.eval('cmd2')
            except exceptions.NotMatchingCommandFoundError:
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

    with describe('when autocompleting or matching lines'):
        with it('pass context to the type'):

            self.interpreter.push_context('context1', prompt='prompt1')
            fake_type = Spy(basic_types.BaseType)
            self._add_command([fake_type], lambda x: None, context_name='context1')
            
            when(fake_type).complete(ANY_ARG).returns([])
            when(fake_type).partial_match(ANY_ARG).returns(True)

            actual_context = self.interpreter.actual_context()

            self.interpreter.complete('test')
            assert_that(fake_type.partial_match, called().with_args('test', actual_context, partial_line=['test']))
            assert_that(fake_type.complete, called().with_args(['test'], actual_context))
            assert_that(fake_type.match, called().with_args('test', actual_context, partial_line=['test']))

