"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    # >>> calculate_days('2021-10-07')   for this example today is 6 october 2021
    -1
    # >>> calculate_days('2021-10-05')
    1
    # >>> calculate_days('10-07-2021')
    WrongFormatException
"""
import pytest
from datetime import datetime, date
from freezegun import freeze_time


class WrongFormatException(Exception):
    pass

@pytest.mark.parametrize("input,expected",  [('2021-10-07',-1), ('2021-10-05',1),('10-07-20-21','WrongFormatException')])
def test_eval(input,expected):
    try:
        days = calculate_days(input)
        assert days == expected
    except WrongFormatException:
        with pytest.raises(WrongFormatException) as excinfo:
            calculate_days(input)
            assert excinfo.value.message == "WrongFormatException"

def calculate_days(from_date: str):
    date_format = '%Y-%m-%d'
    try:
        date = datetime.strptime(from_date, date_format)
        with freeze_time("2021-10-06"):
            now = datetime.now()
        return (date.day - now.day) * -1
    except ValueError:
        raise WrongFormatException('Wrong date format')


print(calculate_days('2022-10-04'))

"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""

# Test

