# -*- coding: utf-8 -*-

from hamcrest import has_length, contains_string, has_items, string_contains_in_order, contains
from doublex import assert_that, is_, Spy, when

from boscli import basic_types

with describe('Or type'):
    with before.each:
        self.type1 = Spy(basic_types.BaseType)
        self.type2 = Spy(basic_types.BaseType)
        self.type3 = Spy(basic_types.BaseType)
        self.context = 'irrelevant_context'
        self.or_type = basic_types.OrType(self.type1, self.type2, self.type3)

    with it('autocomplete with all the types autocompletions'):
        when(self.type1).complete('token', ['token'], self.context).returns(['irrelevant_res1'])
        when(self.type2).complete('token', ['token'], self.context).returns(['irrelevant_res2'])
        when(self.type3).complete('token', ['token'], self.context).returns(['irrelevant_res3'])

        result = self.or_type.complete('token', ['token'], self.context)

        assert_that(result, contains('irrelevant_res1', 'irrelevant_res2', 'irrelevant_res3'))

    with it('matchs if any of the types matchs'):
        when(self.type1).match('token', self.context, partial_line=['token']).returns(False)
        when(self.type2).match('token', self.context, partial_line=['token']).returns(True)
        when(self.type3).match('token', self.context, partial_line=['token']).returns(False)

        result = self.or_type.match('token', self.context, partial_line=['token'])

        assert_that(result, is_(True))

    with it('does not matchs when none matchs'):
        when(self.type1).match('token', self.context, partial_line=['token']).returns(False)
        when(self.type2).match('token', self.context, partial_line=['token']).returns(False)
        when(self.type3).match('token', self.context, partial_line=['token']).returns(False)

        result = self.or_type.match('token', self.context, partial_line=['token'])

        assert_that(result, is_(False))

    with it('partial matchs if any of the types matchs'):
        when(self.type1).partial_match('token', self.context, partial_line=['token']).returns(False)
        when(self.type2).partial_match('token', self.context, partial_line=['token']).returns(True)
        when(self.type3).partial_match('token', self.context, partial_line=['token']).returns(False)

        result = self.or_type.partial_match('token', self.context, partial_line=['token'])

        assert_that(result, is_(True))

    with it('does not partial matchs when none matchs'):
        when(self.type1).partial_match('token', self.context, partial_line=['token']).returns(False)
        when(self.type2).partial_match('token', self.context, partial_line=['token']).returns(False)
        when(self.type3).partial_match('token', self.context, partial_line=['token']).returns(False)

        result = self.or_type.partial_match('token', self.context, partial_line=['token'])

        assert_that(result, is_(False))

    with context('Representation'):
        with context('when name provided'):
            with it('contains the name at its representation'):
                or_type = basic_types.OrType(self.type1, self.type2, self.type3, name='name')

                assert_that(str(or_type), contains_string('name'))



with describe('Basic Types'):

    with before.each:
        self.options_type = basic_types.OptionsType(['op1', 'op2'])
        self.string_type = basic_types.StringType(name='String')
        self.regex_type = basic_types.RegexType('op[1-3]', name='ops1-3')
        self.integer_type = basic_types.IntegerType(min=5, max=10)
        self.context = 'irrelevant_context'


    with context('Options types'):

        with it('autocomplete with options'):
            assert_that(self.options_type.complete('', [''], self.context), has_items(('op1', True), ('op2', True)))

        with it('match if word in valid options'):
            assert_that(self.options_type.match('op1', self.context), is_(True))

        with it('does not math if word not in valid options'):
            assert_that(self.options_type.match('invalid_option', self.context), is_(False))


        with it('partial match if word starts like any valid options'):
            assert_that(self.options_type.partial_match('o', self.context), is_(True))

        with it('does not partial match if word does not starts like any valid options'):
            assert_that(self.options_type.partial_match('inv', self.context), is_(False))

        with context('Representation'):
            with it('include options at its representation'):
                assert_that(str(self.options_type), string_contains_in_order('op1', 'op2'))

            with context('when name provided'):
                with it('string type include its name at its representation'):
                    options_type = basic_types.OptionsType(['op1', 'op2'], name='name')
                    assert_that(str(options_type), contains_string('name'))


    with context('String types'):

        with it('string type has no autocompletion'):
            assert_that(self.string_type.complete('', [''], self.context), has_length(0))

        with it('match always'):
            assert_that(self.string_type.match('', self.context), is_(True))
            assert_that(self.string_type.match('whatever', self.context), is_(True))
            assert_that(self.string_type.match('1', self.context), is_(True))

        with it('partial match always'):
            assert_that(self.string_type.partial_match('', self.context), is_(True))
            assert_that(self.string_type.partial_match('whatever', self.context), is_(True))
            assert_that(self.string_type.partial_match('1', self.context), is_(True))

        with context('Representation'):
            with it('has a default representation'):
                assert_that(str(basic_types.StringType()), contains_string('StringType'))

            with context('when name provided'):
                with it('has name as representation'):
                    assert_that(str(basic_types.StringType(name='name')), contains_string('name'))


    with context('Integer types'):

        with it('integer type has no autocompletion'):
            assert_that(self.integer_type.complete('', [''], self.context), has_length(0))

        with it('does not match strings'):
            assert_that(self.integer_type.match('whatever', self.context), is_(False))

        with describe('when min limit defined'):
            with it('match any number greater than limit'):
                assert_that(self.integer_type.match('5', self.context), is_(False))
                assert_that(self.integer_type.match('6', self.context), is_(True))
            with it('partial match any number greater than limit'):
                assert_that(self.integer_type.partial_match('5', self.context), is_(False))
                assert_that(self.integer_type.partial_match('6', self.context), is_(True))

        with describe('when max limit defined'):
            with it('match any number lesser than limit'):
                assert_that(self.integer_type.match('10', self.context), is_(False))
                assert_that(self.integer_type.match('6', self.context), is_(True))
            with it('partial match any number greater than limit'):
                self.integer_type = basic_types.IntegerType(max=10)
                assert_that(self.integer_type.partial_match('10', self.context), is_(False))
                assert_that(self.integer_type.partial_match('6', self.context), is_(True))

        with context('Representation'):
            with it('has a default representation'):
                assert_that(str(basic_types.IntegerType()), contains_string('IntegerType'))

            with context('when name provided'):
                with it('has name as representation'):
                    assert_that(str(basic_types.IntegerType(name='name')), contains_string('name'))


    with context('Regex types'):
        with it('regex type has no autocompletion'):
            assert_that(self.regex_type.complete('', [''], self.context), has_length(0))

        with it('match when the regexp match'):
            assert_that(self.regex_type.match('op1', self.context), is_(True))
            assert_that(self.regex_type.match('op2', self.context), is_(True))
            assert_that(self.regex_type.match('op3', self.context), is_(True))
            assert_that(self.regex_type.match('op4', self.context), is_(False))

        with it('partial match when the regexp match'):
            assert_that(self.regex_type.partial_match('op1', self.context), is_(True))
            assert_that(self.regex_type.partial_match('op2', self.context), is_(True))
            assert_that(self.regex_type.partial_match('op3', self.context), is_(True))
            assert_that(self.regex_type.partial_match('op4', self.context), is_(False))

        with context('Representation'):
            with it('has a default representation'):
                assert_that(str(basic_types.RegexType('regEx')), contains_string('RegexType'))

            with context('when name provided'):
                with it('has name as representation'):
                    assert_that(str(basic_types.RegexType('regEx', name='name')), contains_string('name'))
