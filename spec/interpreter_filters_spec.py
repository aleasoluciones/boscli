# -*- coding: utf-8 -*-

from mamba import describe, before, context
from doublex import Spy, Stub, assert_that, called

import boscli
from boscli import exceptions, basic_types
from boscli import interpreter as interpreter_module


with describe('Interpreter filters') as _:

    @before.each
    def set_up():
        _.filter_factory = Spy()
        _.output_stream = Stub()
        _.interpreter = interpreter_module.Interpreter(
                                                        filter_factory=_.filter_factory,
                                                        output_stream=_.output_stream)
        _.cmds_implementation = Spy()
        _add_command(['cmd', 'key'], _.cmds_implementation.cmd)


    def _add_command(tokens, func):
        _.interpreter.add_command(boscli.Command(tokens, func))

    with context('malformed line'):
        def it_raise_sintax_error_when_two_filters():
            try:
                _.interpreter.eval('cmd key | include regexp | exclude regexp')
            except exceptions.SintaxError:
                pass

        def it_raise_sintax_error_when_incomplete_filter():
            try:
                _.interpreter.eval('cmd key | include')
            except exceptions.SintaxError:
                pass

        def it_raise_sintax_error_when_unknown_filter():
            try:
                _.interpreter.eval('cmd key | unknown_filter regexp')
            except exceptions.SintaxError:
                pass

    with context('command execution'):

        with describe('when include filter used'):

            def it_executed_command_connected_to_include_filter():
                _.interpreter.eval('cmd key | include regexp')

                assert_that(_.cmds_implementation.cmd,
                                        called().with_args(tokens=['cmd', 'key'], interpreter=_.interpreter))

            def it_create_include_filter_connected_to_output_stream():
                _.interpreter.eval('cmd key | include regexp')
                assert_that(_.filter_factory.create_include_filter,
                                        called().with_args('regexp', _.output_stream))


        with describe('when exclude filter used'):

            def it_executed_command_connected_to_exclude_filter():
                _.interpreter.eval('cmd key | exclude regexp')

                assert_that(_.cmds_implementation.cmd,
                                        called().with_args(tokens=['cmd', 'key'], interpreter=_.interpreter))

            def it_creates_exclude_filter_connected_to_output_stream():
                _.interpreter.eval('cmd key | exclude regexp')
                assert_that(_.filter_factory.create_exclude_filter,
                                        called().with_args('regexp', _.output_stream))
