from ui.validator import *


class TestValidYear:
    def test_norm_value(self):
        answer = 1
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
        answer = 0
        result = valid_year(None)
        assert result == answer

