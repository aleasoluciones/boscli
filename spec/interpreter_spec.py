# -*- coding: utf-8 -*-

from hamcrest import none, has_length, has_items, is_not, is_
from doublex import Spy, assert_that, called, Stub, when, ANY_ARG

import boscli
from boscli import exceptions, basic_types
from boscli import interpreter as interpreter_module
from boscli.command import Command

with describe('Interpreter'):
    with before.each:
        self.interpreter = interpreter_module.Interpreter()
        self.cmds_implementation = Spy()
        self._add_command(['cmd', 'key'], self.cmds_implementation.cmd)
        self._add_command(['cmd_with_parameters', basic_types.StringType(), basic_types.StringType()],
                                self.cmds_implementation.cmd_with_parameters)
        self._add_command(['cmd_with_ops', basic_types.OptionsType(['op1', 'op2'])],
                                self.cmds_implementation.cmd_with_ops)
        self._add_command(['cmd_with_regex', basic_types.RegexType('^start.*')],
                                self.cmds_implementation.cmd_with_regex)

    def _add_command(self, tokens, func):
        self.interpreter.add_command(Command(tokens, func))

    with context('command execution'):
        with describe('when evaluating multiple lines'):
            with it('execute each line / command'):
                lines = ['cmd key', 'cmd_with_parameters s1 s2']
                self.interpreter.eval_multiple(lines)

                assert_that(self.cmds_implementation.cmd,
                                        called().with_args(tokens=['cmd', 'key'], interpreter=self.interpreter))
                assert_that(self.cmds_implementation.cmd_with_parameters,
                                        called().with_args('s1', 's2', tokens=['cmd_with_parameters', 's1', 's2'], interpreter=self.interpreter))

            with it('returns the result for each line'):
                when(self.cmds_implementation).cmd(ANY_ARG).returns('a_result')
                lines = ['cmd key', 'cmd_with_parameters s1 s2']

                result = self.interpreter.eval_multiple(lines)

                assert_that(result, has_items('a_result', None))


        with describe('when evaluating emptyline'):
            with it('returns_none'):
                assert_that(self.interpreter.eval(''), none())

        with describe('when all keyword match'):
            with it('executes command'):
                self.interpreter.eval('cmd key')

                assert_that(self.cmds_implementation.cmd,
                                        called().with_args(tokens=['cmd', 'key'], interpreter=self.interpreter))

        with describe('ctrl+c when running a command'):
            with it('stops the command'):
                def an_interrupted_cmd(*args, **kwargs):
                    self.cmds_implementation.cmd1()
                    raise KeyboardInterrupt()
                    self.cmds_implementation.cmd2()

                self._add_command(['cmd', 'ctrl+c'], an_interrupted_cmd)

                self.interpreter.eval("cmd ctrl+c")

                assert_that(self.cmds_implementation.cmd1, called())
                assert_that(self.cmds_implementation.cmd2, is_not(called()))

        with describe('when all keyword partial match'):
            with it('executes command'):
                self.interpreter.eval('cm ke')

                assert_that(self.cmds_implementation.cmd,
                                        called().with_args(tokens=['cmd', 'key'], interpreter=self.interpreter))

        with describe('when a line does not match any command'):
            with it('raises exception'):
                try:
                    self.interpreter.eval('unknown command')
                except exceptions.NoMatchingCommandFoundError:
                    pass

        with describe('when two command matchs'):
            with it('raises ambiguous command exception with the commands information'):
                try:
                    cmd1 = Command(['ambigous_cmd1'], Stub().cmd1)
                    self.interpreter.add_command(cmd1)
                    cmd2 = Command(['ambigous_cmd2'], Stub().cmd2)
                    self.interpreter.add_command(cmd2)

                    self.interpreter.eval('ambigous_cmd')

                    assert False, "Should raise AmbiguousCommandError"

                except exceptions.AmbiguousCommandError as exc:
                    assert_that(exc.matching_commands, has_length(2))
                    assert_that(exc.matching_commands, has_items(cmd1, cmd2))

        with context('string parameters'):
            with describe('when two string parameters are given'):

                with it('executes command passing the parameters'):
                    self.interpreter.eval('cmd_with_parameters param1 param2')

                    assert_that(self.cmds_implementation.cmd_with_parameters,
                                            called().with_args('param1', 'param2',
                                                                tokens=['cmd_with_parameters', 'param1', 'param2'],
                                                                interpreter=self.interpreter))


            with describe('when string parameters use quotes'):
                with it('can contains spaces inside'):
                    self.interpreter.eval('cmd_with_parameters param1 "param with spaces"')

                    assert_that(self.cmds_implementation.cmd_with_parameters,
                                            called().with_args('param1', "param with spaces",
                                                                tokens=['cmd_with_parameters', 'param1', "param with spaces"],
                                                                interpreter=self.interpreter))
        with context('options parameters'):

            with describe('when a valid option is given'):
                with it('execute the command with the given option'):
                    self.interpreter.eval('cmd_with_ops op1')

                    assert_that(self.cmds_implementation.cmd_with_ops,
                                            called().with_args('op1',
                                                                                    tokens=['cmd_with_ops', 'op1'],
                                                                                    interpreter=self.interpreter))

            with describe('when a invalid option is given'):
                with it('not excute the command'):
                    try:
                        self.interpreter.eval('cmd_with_ops invalid_op')

                    except exceptions.NoMatchingCommandFoundError:
                        pass

        with context('regex parameter'):

            with describe('when parameter match with defined regex'):
                with it('execute the command passing the given regex'):

                    self.interpreter.eval('cmd_with_regex start_whatever')

                    assert_that(self.cmds_implementation.cmd_with_regex,
                                            called().with_args('start_whatever',
                                                                                    tokens=['cmd_with_regex', 'start_whatever'],
                                                                                    interpreter=self.interpreter))

            with describe('when parameter does not match with defined regex'):
                with it('not execute any command'):

                    try:
                        self.interpreter.eval('cmd_with_regex not_matching_parameter')
                    except exceptions.NoMatchingCommandFoundError:
                        pass

    with context('command execution (using abbreviations for keywords'):
        with describe('when all keyword are abbreviated'):
            with it('executes command'):
                self.interpreter.eval('cm ke')

                assert_that(self.cmds_implementation.cmd,
                                        called().with_args(tokens=['cmd', 'key'], interpreter=self.interpreter))
        with describe('when only a keyword is abbreviated'):
            with it('executes command'):
                self.interpreter.eval('cmd ke')

                assert_that(self.cmds_implementation.cmd,
                                        called().with_args(tokens=['cmd', 'key'], interpreter=self.interpreter))


        with describe('when two command matchs (the abbreviated keyword)'):
            with it('raises ambiguous command exception'):
                try:
                    self._add_command(['configure'], Stub().cmd1)
                    self._add_command(['consolidate'], Stub().cmd2)
                    self.interpreter.eval('con')
                except exceptions.AmbiguousCommandError:
                    pass
                else:
                    assert False, 'expected AmbiguousCommandError raised'

        with describe('when there is a perfect match and a match with abbreviated keyword'):
            with it('executed perfect matching command'):

                command = Spy()
                self._add_command(['keyword1'], self.cmds_implementation.perfect_match)
                self._add_command(['keyword1.1'], self.cmds_implementation.normal_match)

                self.interpreter.eval('keyword1')

                assert_that(self.cmds_implementation.perfect_match,
                            called().with_args(tokens=['keyword1'], interpreter=self.interpreter))

    with context('command execution with autoexpansion of parameters'):
        with describe('when there is a uniq autocompletion'):
            with it('expand the parameter to the autocompletion and execute the command'):
                self._add_command(['cmd1', basic_types.OptionsType(['firstOp', 'secondOp'])],
                                self.cmds_implementation.cmd1)

                self.interpreter.eval('cmd1 first')

                assert_that(self.cmds_implementation.cmd1,
                                        called().with_args('firstOp', tokens=['cmd1', 'firstOp'], interpreter=self.interpreter))

            with it('expand all parameters with uniques autocompletions and execute the command'):

                self._add_command(['cmd1', basic_types.OptionsType(['firstOp', 'secondOp']), basic_types.OptionsType(['firstOp', 'secondOp'])],
                                self.cmds_implementation.cmd1)

                self.interpreter.eval('cmd1 first second')

                assert_that(self.cmds_implementation.cmd1,
                                        called().with_args('firstOp', 'secondOp', tokens=['cmd1', 'firstOp', 'secondOp'], interpreter=self.interpreter))

    with context('prompt management'):
        with describe('when we are at the initial context'):
            with it('have a default prompt'):
                assert_that(self.interpreter.prompt, is_('Default'))

            with it('allow change the prompt'):
                self.interpreter.prompt = 'prompt1'

                assert_that(self.interpreter.prompt, is_('prompt1'))

            with it('maintain the prompts of previous contexts'):
                self.interpreter.prompt = 'default'

                assert_that(self.interpreter.prompt, is_('default'))

                self.interpreter.push_context('context1', "prompt_context1")
                assert_that(self.interpreter.prompt, is_('prompt_context1'))

                self.interpreter.push_context('context2', "prompt_context2")
                assert_that(self.interpreter.prompt, is_('prompt_context2'))

                self.interpreter.pop_context()
                assert_that(self.interpreter.prompt, is_('prompt_context1'))

                self.interpreter.pop_context()
                assert_that(self.interpreter.prompt, is_('default'))

with describe('Interpreter parse mode'):
    with before.each:
        self.interpreter = interpreter_module.Interpreter()
        self.interpreter.add_command(Command(['cmd', 'key1'], Spy().irrelevant_func, cmd_id='id1'))
        self.interpreter.add_command(Command(['cmd', 'key2'],  Spy().irrelevant_func, cmd_id='id2'))

    with it('parse a line'):
        result1 = self.interpreter.parse('cmd key1')
        result2 = self.interpreter.parse('cmd key2')

        assert_that(result1, is_('id1'))
        assert_that(result2, is_('id2'))

    with it('parse a line with spaces'):
        result = self.interpreter.parse(' cmd key1 ')

        assert_that(result, is_('id1'))

    with it('return None for the empty line'):
        result = self.interpreter.parse('')

        assert_that(result, is_(None))

    with it('raise an exception if there is no match'):
        try:
            self.interpreter.eval('unknown command')
            assert False, "Should raise NoMatchingCommandFoundError"
        except exceptions.NoMatchingCommandFoundError:
            pass
        except Exception as ex:
            assert False, f"Should raise NoMatchingCommandFoundError, but {type(ex)}"
