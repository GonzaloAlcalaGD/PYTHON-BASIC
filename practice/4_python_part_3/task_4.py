"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
from faker import Faker
from unittest.mock import Mock, patch
import pytest


my_parser = argparse.ArgumentParser(prog='task_4.py',
                                    usage='$python %(prog)s NUMBER --FIELD=fake_address --FIELD=some_name',
                                    argument_default=None,
                                    add_help=True,
                                    description='Generate fake names and fake directions',
                                    epilog='Enjoy!')

my_parser.add_argument('NUMBER', help='positive number of generated instances', type=int)
my_parser.add_argument('FIELD', help='key used in generated dict', type=str)
my_parser.add_argument('PROVIDER', help='name of Faker provider', type=str)

args = my_parser.parse_args()
number = args.NUMBER
field = args.FIELD
provider = args.PROVIDER

fake = Faker()

def print_name_address(args: argparse.Namespace) -> None:
    global field, provider
    for _ in range(args):
        print(gen_dict(field, provider))


def gen_dict(field, provider):
    my_dict = {field: fake.name(), provider: fake.address()}
    return my_dict


# print_name_address(number)

"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""

# Test
input_mock = Mock()
output_mock = Mock()
# output.method.return_value = {"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}

@pytest.fixture
def cli_args():
    input_mock.method.return_value = 'task_4.py 2 --fake-address=address --some_name=name'
    return input_mock


def test_gen_dict(monkeypatch, cli_args):
    assert True
