from hamcrest import assert_that
from doublex import Spy, called, never

from boscli import filters


with describe('Filters'):

    with before.each:
        self.output_stream  = Spy()
        self.include_filter = filters.IncludeFilter('regex', self.output_stream)
        self.exclude_filter = filters.ExcludeFilter('regex', self.output_stream)

    with describe('when the line include regex'):
        with it('include filter output the line'):
            self.include_filter.write('line including regex \n')
            assert_that(self.output_stream.write, called().with_args('line including regex \n'))

        with it('exclude filter does not output the line'):
            self.exclude_filter.write('line including regex \n')
            assert_that(self.output_stream.write, never(called().with_args('line including regex \n')))

    with describe('when the line does not include regex'):
        with it('include filter does not output the line'):
            self.include_filter.write('line \n')
            assert_that(self.output_stream.write, never(called().with_args('line including regex \n')))

        with it('exclude filter output the line'):
            self.exclude_filter.write('line \n')
            assert_that(self.output_stream.write, called().with_args('line \n'))

    with describe('when write chunks of data to the filter'):
        with it('include filter process data line by line'):
            self.include_filter.write('begin ')
            self.include_filter.write('regex ')
            self.include_filter.write('end\n')
            assert_that(self.output_stream.write, called().with_args('begin regex end\n'))

        def exclude_filter_process_data_line_by_line():
            self.exclude_filter.write('begin ')
            self.exclude_filter.write('end\n')
            assert_that(self.output_stream.write, called().with_args('begin end\n'))
