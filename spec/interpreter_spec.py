# -*- coding: utf-8 -*-

from mamba import *
from hamcrest import *
from doublex import *

import boscli
from boscli import exceptions, basic_types
from boscli import interpreter as interpreter_module


with describe('Interpreter') as _:

	@before.each
	def set_up():
		_.interpreter = interpreter_module.Interpreter()
		_.cmds_implementation = Spy()
		_add_command(['cmd', 'key'], _.cmds_implementation.cmd)
		_add_command(['cmd_with_parameters', basic_types.StringType(), basic_types.StringType()],
					_.cmds_implementation.cmd_with_parameters)
		_add_command(['cmd_with_ops', basic_types.OptionsType(['op1', 'op2'])],
					_.cmds_implementation.cmd_with_ops)
		_add_command(['cmd_with_regex', basic_types.RegexType('^start.*')],
					_.cmds_implementation.cmd_with_regex)

	def _add_command(tokens, func):
		_.interpreter.add_command(boscli.Command(tokens, func))

	with context('command execution'):

		with describe('when evaluating emptyline'):
			def it_returns_none():
				assert_that(_.interpreter.eval(''), none())

		with describe('when all keyword match'):
			def it_executes_command():
				_.interpreter.eval('cmd key')

				assert_that(_.cmds_implementation.cmd, 
							called().with_args(tokens=['cmd', 'key'], interpreter=_.interpreter))

		with describe('when a line does not match any command'):
			def it_raises_exception():
				try:
					_.interpreter.eval('unknown command')
				except exceptions.NotMatchingCommandFoundError:
					pass

		with describe('when two command matchs'):
			def it_raises_ambiguous_command_exception():
				try:
					_add_command(['ambigous_cmd'], Stub().cmd1)
					_add_command(['ambigous_cmd'], Stub().cmd2)
					_.interpreter.eval('ambigous_cmd')
				except exceptions.AmbiguousCommandError:
					pass

		with context('string parameters'):
			with describe('when two string parameters are given'):

				def it_executes_command_passing_the_parameters():
					_.interpreter.eval('cmd_with_parameters param1 param2')

					assert_that(_.cmds_implementation.cmd_with_parameters,
								called().with_args('param1', 'param2',
													tokens=['cmd_with_parameters', 'param1', 'param2'],
													interpreter=_.interpreter))


			with describe('when string parameters use quotes'):
				def it_can_contains_spaces_inside():
					_.interpreter.eval('cmd_with_parameters param1 "param with spaces"')

					assert_that(_.cmds_implementation.cmd_with_parameters,
								called().with_args('param1', "param with spaces",
													tokens=['cmd_with_parameters', 'param1', "param with spaces"],
													interpreter=_.interpreter))
		with context('options parameters'):

			with describe('when a valid option is given'):
				def it_execute_the_command_with_the_given_option():
					_.interpreter.eval('cmd_with_ops op1')

					assert_that(_.cmds_implementation.cmd_with_ops,
								called().with_args('op1',
													tokens=['cmd_with_ops', 'op1'],
													interpreter=_.interpreter))

			with describe('when a invalid option is given'):
				def it_not_excute_the_command():
					try:
						_.interpreter.eval('cmd_with_ops invalid_op')

					except exceptions.NotMatchingCommandFoundError:
						pass

		with context('regex parameter'):

			with describe('when parameter match with defined regex'):
				def it_execute_the_command_passing_the_given_regex():

					_.interpreter.eval('cmd_with_regex start_whatever')
					
					assert_that(_.cmds_implementation.cmd_with_regex,
								called().with_args('start_whatever',
													tokens=['cmd_with_regex', 'start_whatever'],
													interpreter=_.interpreter))

			with describe('when parameter does not match with defined regex'):
				def it_not_execute_any_command():

					try:
						_.interpreter.eval('cmd_with_regex not_matching_parameter')
						pass
					except exceptions.NotMatchingCommandFoundError:
						pass
					