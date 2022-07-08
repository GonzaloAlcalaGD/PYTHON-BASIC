"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""
import math
import pytest


class OperationNotFoundException(Exception):
    print('Operation not found')


def math_calculate(function: str, *args):
    if not function in ['log', 'ceil']:
        OperationNotFoundException()
    elif function == 'log':
        return math.log(*args)
    else:
        return math.ceil(*args)


print(math_calculate('ceil', 10.7))
"""
Write tests for math_calculate function
"""


@pytest.fixture
def set_log():
    return 'log', 1024, 4


@pytest.fixture
def set_ceil():
    return 'ceil', 10.7


@pytest.fixture
def set_failure():
    return 'division', 2, 12


# Test


def test_log(set_log):
    assert math_calculate(set_log) == 5.0


def test_math(set_ceil):
    assert math_calculate(set_ceil) == 11


def test_failure(set_failure):
    with pytest.raises(Exception) as exception_info:
        OperationNotFoundException()
    assert exception_info.value.message == 'Operation not found'

