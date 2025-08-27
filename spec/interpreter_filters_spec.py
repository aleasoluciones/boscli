from doublex import Spy, Stub, assert_that, called

from boscli import exceptions
from boscli import interpreter as interpreter_module
from boscli.command import Command


with describe('Interpreter filters'):

    with before.each:
        self.filter_factory = Spy()
        self.output_stream = Stub()
        self.interpreter = interpreter_module.Interpreter(filter_factory=self.filter_factory,
                                                          output_stream=self.output_stream)
        self.cmds_implementation = Spy()
        self._add_command(['cmd', 'key'], self.cmds_implementation.cmd)


    def _add_command(self, tokens, func):
        self.interpreter.add_command(Command(tokens, func))

    with context('malformed line'):
        with it('raise sintax error when two filters'):
            try:
                self.interpreter.eval('cmd key | include regexp | exclude regexp')
            except exceptions.SyntaxError:
                pass

        with it('raise sintax error when incomplete filter'):
            try:
                self.interpreter.eval('cmd key | include')
            except exceptions.SyntaxError:
                pass

        with it('raise sintax error when unknown filter'):
            try:
                self.interpreter.eval('cmd key | unknown_filter regexp')
            except exceptions.SyntaxError:
                pass

    with context('command execution'):
        with describe('when include filter used'):
            with it('executed command connected to include filter'):
                self.interpreter.eval('cmd key | include regexp')

                self._assert_command_called_with_filter_connected_to_output(self.filter_factory.create_include_filter)

        with describe('when abbreviated include keyword used'):
            with it('executed command connected to include filter'):
                self.interpreter.eval('cmd key | inc regexp')

                self._assert_command_called_with_filter_connected_to_output(self.filter_factory.create_include_filter)

        with describe('when exclude filter used'):
            with it('executed command connected to exclude filter'):
                self.interpreter.eval('cmd key | exclude regexp')

                self._assert_command_called_with_filter_connected_to_output(self.filter_factory.create_exclude_filter)

        with describe('when abbreviated exclude keyword used'):
            with it('executed command connected to exclude filter'):
                self.interpreter.eval('cmd key | exc regexp')

                self._assert_command_called_with_filter_connected_to_output(self.filter_factory.create_exclude_filter)


        def _assert_command_called_with_filter_connected_to_output(self, create_filter_method):
                assert_that(self.cmds_implementation.cmd,
                            called().with_args(tokens=['cmd', 'key'], interpreter=self.interpreter))
                assert_that(create_filter_method,
                            called().with_args('regexp', self.output_stream))