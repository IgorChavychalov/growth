from ui.validator import *


class TestValidYear:
    def test_norm_value(self):
        answer = 1111
        result = valid_year('1111')
        assert result == answer

    def test_random_char_in_value(self):
        answer = 0
        result = valid_year('111k')
        assert result == answer

    def test_last_space_in_value(self):
        answer = 0
        result = valid_year('1118 ')
        assert result == answer

    def test_random_point_in_value(self):
        answer = 0
        result = valid_year('1.118')
        assert result == answer

    def test_none_value(self):
        answer = None
        result = valid_year(None)
        assert result == answer


class TestVlideCreateForm:
    def test_years_field(self):
        answer = True
        args = ['fff', '234', '12,13', '1111', '1111', '1111', '1111']
        result = validate_create_form(args)

    def test_miss_digit_years_field(self):
        answer = False
        args = ['fff', '234', '12,13', '1111', '111', '1111', '1111']
        result = validate_create_form(args)

    def test_miss_years_field(self):
        answer = True
        args = ['fff', '234', '12,13', None, None, None, None]
        result = validate_create_form(args)














