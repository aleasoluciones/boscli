# -*- coding: utf-8 -*-

from hamcrest import has_length, contains_string, has_items, string_contains_in_order
from doublex import assert_that, is_

from boscli import basic_types


with describe('Basic Types'):

    with before.each:
        self.options_type = basic_types.OptionsType(['op1', 'op2'])
        self.string_type = basic_types.StringType(name='String')
        self.regex_type = basic_types.RegexType('op[1-3]', name='ops1-3')

    with context('Options types'):

        with it('autocomplete with options'):
            assert_that(self.options_type.complete(['']), has_items('op1', 'op2'))

        with it('match if word in valid options'):
            assert_that(self.options_type.match('op1'), is_(True))

        with it('does not math if word not in valid options'):
            assert_that(self.options_type.match('invalid_option'), is_(False))

        with it('include options at its representation'):
            assert_that(str(self.options_type), string_contains_in_order('op1', 'op2'))

        with it('partial match if word starts like any valid options'):
            assert_that(self.options_type.partial_match('o'), is_(True))

        with it('does not partial match if word does not starts like any valid options'):
            assert_that(self.options_type.partial_match('inv'), is_(False))

    with context('String types'):

        with it('string type has no autocompletion'):
            assert_that(self.string_type.complete(['']), has_length(0))

        with it('match always'):
            assert_that(self.string_type.match(''), is_(True))
            assert_that(self.string_type.match('whatever'), is_(True))
            assert_that(self.string_type.match('1'), is_(True))

        with it('partial match always'):
            assert_that(self.string_type.partial_match(''), is_(True))
            assert_that(self.string_type.partial_match('whatever'), is_(True))
            assert_that(self.string_type.partial_match('1'), is_(True))

        with it('string type include its name at its representation'):
            assert_that(str(self.string_type), contains_string('String'))


    with context('Regex types'):
        with it('regex type has no autocompletion'):
            assert_that(self.regex_type.complete(['']), has_length(0))

        with it('match when the regexp match'):
            assert_that(self.regex_type.match('op1'), is_(True))
            assert_that(self.regex_type.match('op2'), is_(True))
            assert_that(self.regex_type.match('op3'), is_(True))
            assert_that(self.regex_type.match('op4'), is_(False))

        with it('partial match when the regexp match'):
            assert_that(self.regex_type.partial_match('op1'), is_(True))
            assert_that(self.regex_type.partial_match('op2'), is_(True))
            assert_that(self.regex_type.partial_match('op3'), is_(True))
            assert_that(self.regex_type.partial_match('op4'), is_(False))

        with it('regex type include its name at its representation'):
            assert_that(str(self.regex_type), contains_string('ops1-3'))
