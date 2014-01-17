# -*- coding: utf-8 -*-

from mamba import *
from hamcrest import *
from doublex import *

from boscli import filters



with describe('Filters') as _:

	@before.each
	def set_up():
		_.output_stream  = Spy()
		_.include_filter = filters.IncludeFilter('regex', _.output_stream)
		_.exclude_filter = filters.ExcludeFilter('regex', _.output_stream)
	
	with describe('when the line include regex'):
		
		def it_include_filter_output_the_line():
			_.include_filter.write('line including regex \n')
			assert_that(_.output_stream.write, called().with_args('line including regex \n'))

		def it_exclude_filter_does_not_output_the_line():
			_.exclude_filter.write('line including regex \n')
			assert_that(_.output_stream.write, never(called().with_args('line including regex \n')))

	with describe('when the line does not include regex'):
		
		def it_include_filter_does_not_output_the_line():
			_.include_filter.write('line \n')
			assert_that(_.output_stream.write, never(called().with_args('line including regex \n')))

		def it_exclude_filter_output_the_line():
			_.exclude_filter.write('line \n')
			assert_that(_.output_stream.write, called().with_args('line \n'))

	with describe('when write chunks of data to the filter'):
		
		def include_filter_process_data_line_by_line():
			_.include_filter.write('begin ')
			_.include_filter.write('regex ')
			_.include_filter.write('end\n')
			assert_that(_.output_stream.write, called().with_args('begin regex end\n'))

		def exclude_filter_process_data_line_by_line():
			_.exclude_filter.write('begin ')
			_.exclude_filter.write('end\n')
			assert_that(_.output_stream.write, called().with_args('begin end\n'))


