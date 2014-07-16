# -*- coding: utf-8 -*-

from doublex import Spy, Stub, assert_that, called

from boscli import exceptions
from boscli import interpreter as interpreter_module
from boscli.command import Command


with describe('Interpreter filters'):

    with before.each:
        self.filter_factory = Spy()
        self.output_stream = Stub()
        self.interpreter = interpreter_module.Interpreter(
                                                        filter_factory=self.filter_factory,
                                                        output_stream=self.output_stream)
        self.cmds_implementation = Spy()
        self._add_command(['cmd', 'key'], self.cmds_implementation.cmd)


    def _add_command(self, tokens, func):
        self.interpreter.add_command(Command(tokens, func))

    with context('malformed line'):
        with it('raise sintax error when two filters'):
            try:
                self.interpreter.eval('cmd key | include regexp | exclude regexp')
            except exceptions.SintaxError:
                pass

        with it('raise sintax error when incomplete filter'):
            try:
                self.interpreter.eval('cmd key | include')
            except exceptions.SintaxError:
                pass

        with it('raise sintax error when unknown filter'):
            try:
                self.interpreter.eval('cmd key | unknown_filter regexp')
            except exceptions.SintaxError:
                pass

    with context('command execution'):
        with describe('when include filter used'):
            with it('executed command connected to include filter'):
                self.interpreter.eval('cmd key | include regexp')

                assert_that(self.cmds_implementation.cmd,
                                        called().with_args(tokens=['cmd', 'key'], interpreter=self.interpreter))

            with it('create include filter connected to output stream'):
                self.interpreter.eval('cmd key | include regexp')
                assert_that(self.filter_factory.create_include_filter,
                                        called().with_args('regexp', self.output_stream))

        with describe('when exclude filter used'):
            with it('executed command connected to exclude filter'):
                self.interpreter.eval('cmd key | exclude regexp')

                assert_that(self.cmds_implementation.cmd,
                                        called().with_args(tokens=['cmd', 'key'], interpreter=self.interpreter))

            with it('creates exclude filter connected to output stream'):
                self.interpreter.eval('cmd key | exclude regexp')
                assert_that(self.filter_factory.create_exclude_filter,
                                        called().with_args('regexp', self.output_stream))
