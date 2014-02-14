# -*- coding: utf-8 -*-

from mamba import describe, context, before
from hamcrest import has_length, contains_string, has_items, string_contains_in_order
from doublex import assert_that, is_

from boscli import basic_types


with describe('Basic Types') as _:

    @before.each
    def set_up():
        _.options_type = basic_types.OptionsType(['op1', 'op2'])
        _.string_type = basic_types.StringType(name='String')
        _.regex_type = basic_types.RegexType('op[1-3]', name='ops1-3')

    with context('Options types'):

        def it_autocomplete_with_options():
            assert_that(_.options_type.complete(['']), has_items('op1', 'op2'))

        def it_match_if_word_in_valid_options():
            assert_that(_.options_type.match('op1'), is_(True))
        
        def it_does_not_math_if_word_not_in_valid_options():
            assert_that(_.options_type.match('invalid_option'), is_(False))
        
        def it_include_options_at_its_representation():
            assert_that(str(_.options_type), string_contains_in_order('op1', 'op2'))

        def it_partial_match_if_word_starts_like_any_valid_options():
            assert_that(_.options_type.partial_match('o'), is_(True))

        def it_does_not_partial_match_if_word_does_not_starts_like_any_valid_options():
            assert_that(_.options_type.partial_match('inv'), is_(False))


    with context('String types'):

        def it_has_no_autocompletion():
            assert_that(_.string_type.complete(['']), has_length(0))

        def it_match_always():
            assert_that(_.string_type.match(''), is_(True))
            assert_that(_.string_type.match('whatever'), is_(True))
            assert_that(_.string_type.match('1'), is_(True))
        
        def it_partial_match_always():
            assert_that(_.string_type.partial_match(''), is_(True))
            assert_that(_.string_type.partial_match('whatever'), is_(True))
            assert_that(_.string_type.partial_match('1'), is_(True))

        def it_include_its_name_at_its_representation():
            assert_that(str(_.string_type), contains_string('String'))


    with context('Regex types'):
        #_.regex_type = basic_types.RegexType(name='op[1-3]', name='ops1-3')

        def it_has_no_autocompletion():
            assert_that(_.regex_type.complete(['']), has_length(0))

        def it_match_when_the_regexp_match():
            assert_that(_.regex_type.match('op1'), is_(True))
            assert_that(_.regex_type.match('op2'), is_(True))
            assert_that(_.regex_type.match('op3'), is_(True))
            assert_that(_.regex_type.match('op4'), is_(False))
        
        def it_partial_match_when_the_regexp_match():
            assert_that(_.regex_type.partial_match('op1'), is_(True))
            assert_that(_.regex_type.partial_match('op2'), is_(True))
            assert_that(_.regex_type.partial_match('op3'), is_(True))
            assert_that(_.regex_type.partial_match('op4'), is_(False))

        def it_include_its_name_at_its_representation():
            assert_that(str(_.regex_type), contains_string('ops1-3'))

