# -*- coding: utf-8 -*-

from hamcrest import none
from doublex import Spy, assert_that, called, Stub

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
        with describe('when evaluating emptyline'):
            with it('returns_none'):
                assert_that(self.interpreter.eval(''), none())

        with describe('when all keyword match'):
            with it('executes command'):
                self.interpreter.eval('cmd key')

                assert_that(self.cmds_implementation.cmd,
                                        called().with_args(tokens=['cmd', 'key'], interpreter=self.interpreter))

        with describe('when a line does not match any command'):
            with it('raises exception'):
                try:
                    self.interpreter.eval('unknown command')
                except exceptions.NotMatchingCommandFoundError:
                    pass

        with describe('when two command matchs'):
            with it('raises ambiguous command exception'):
                try:
                    self._add_command(['ambigous_cmd'], Stub().cmd1)
                    self._add_command(['ambigous_cmd'], Stub().cmd2)
                    self.interpreter.eval('ambigous_cmd')
                except exceptions.AmbiguousCommandError:
                    pass

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

                    except exceptions.NotMatchingCommandFoundError:
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
                    except exceptions.NotMatchingCommandFoundError:
                        pass
