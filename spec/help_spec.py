# -*- coding: utf-8 -*-

from doublex import Spy
from hamcrest import assert_that, has_entries, has_entry, contains_string, is_not

from boscli import basic_types
from boscli import interpreter as interpreter_module
from boscli.command import Command

with describe('Help'):

    with before.each:
        self.interpreter = interpreter_module.Interpreter()
        self.command_implementation = Spy()
        self.cmd1 = Command(['cmd', 'key1'], self.command_implementation.cmd1, help='help_cmd1', allways=True)
        self.cmd2 = Command(['cmd', 'normal'], self.command_implementation.cmd1, help='help_normal')
        self.cmd_no_help = Command(['description', basic_types.StringType()], self.command_implementation.description)
        self.cmd_context = Command(['cmd', 'key2'], self.command_implementation.netmask, context_name='irrelevant_context', help='help_cmd_context')

        self.interpreter.add_command(self.cmd1)
        self.interpreter.add_command(self.cmd2)
        self.interpreter.add_command(self.cmd_no_help)
        self.interpreter.add_command(self.cmd_context)

    with context('when asking for help with empty line'):
        with describe('when not in a context'):
            with it('returns help for all active commands that not requires a context'):
                result = self.interpreter.help('')
                assert_that(result, has_entries(
                        self.cmd1, contains_string('help_cmd1'), 
                        self.cmd2, contains_string('help_normal'), 
                        self.cmd_no_help, None))
                assert_that(result, is_not(has_entries(self.cmd_context, contains_string('help_cmd_context'))))

        with describe('when inside a context'):
            with it('returns help for commands from the actual context'):
                self.interpreter.push_context('irrelevant_context')

                result = self.interpreter.help('')
                assert_that(result, has_entry(self.cmd_context, contains_string('help_cmd_context')))

            with it('returns help for commands that are allways active'):
                self.interpreter.push_context('irrelevant_context')

                result = self.interpreter.help('')
                assert_that(result, 
                    has_entries(self.cmd1, contains_string('help_cmd1')))

            with it('does not returns help for normal commands (command from main context without allways flag)'):
                self.interpreter.push_context('irrelevant_context')

                result = self.interpreter.help('')
                
                assert_that(result, is_not(has_entries(self.cmd2, contains_string('help_normal'))))
                assert_that(result, is_not(has_entries(self.cmd_no_help, None)))


    with context('when asking for help with a line with a partial command'):
        with it('returns help for partial matching commands'):
            result = self.interpreter.help('cmd ')
            
            assert_that(result, has_entries(
                self.cmd1, contains_string('help_cmd1'),
                self.cmd2, contains_string('help_normal')))
            assert_that(result, is_not(has_entries(self.cmd_no_help, None)))
            assert_that(result, is_not(has_entries(self.cmd_context, contains_string('help_cmd_context'))))
