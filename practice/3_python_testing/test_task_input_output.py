"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""
from unittest.mock import Mock, patch
import pytest

incorrect_input = Mock()
correct_input = Mock()
input_mock = Mock()


def return_input(n):
    test = []
    for _ in range(n):
        user_input = input()
        try:
            test.append(int(user_input))
        except ValueError:
            return 'Failed case'
    return 'Successful case'


def test_read_numbers_without_text_input():
    n = 4
    input_list = [1,2,3,4]
    attr = []
    for _ in range(n):
        correct_mock = Mock()
        correct_mock.return_value = str(input_list[_])
        attr.append(correct_mock.return_value)
    input_mock.side_effect = input_list
    with patch('builtins.input', input_mock) as mock_method:
        result = return_input(n)
    assert result == 'Successful case'


def test_read_numbers_with_text_input():
    n = 3
    input_list = [1, 2, 'text']
    attr = []

    for _ in range(n):
        incorrect_mock = Mock()
        incorrect_mock.return_value = str(input_list[_])
        attr.append(incorrect_mock.return_value)
    input_mock.side_effect = input_list

    with patch('builtins.input', input_mock) as mock_method:
        result = return_input(n)
    assert result == 'Failed case'


