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
import re
import sys

from faker import Faker
from unittest.mock import Mock, patch
import pytest


my_parser = argparse.ArgumentParser(prog='task_4.py',
                                    usage='$python %(prog)s NUMBER --some_name=name',
                                    argument_default=None,
                                    add_help=True,
                                    description='Generate fake names and fake directions',
                                    epilog='Enjoy!')
fake = Faker()


def cli(args: argparse.Namespace) -> None:
    list_dict = []
    args.pop(0)
    items = int(args.pop(0))
    for item in range(items):
        temp = {}
        for argument in args:
            search = re.search(r'[a-z]', argument, re.I)
            if search is not None:
                argument = argument[search.start():]
                key, value = argument.split('=')
                instruction = 'fake.' + str(value) + '()'
                temp[key] = eval(instruction)
        list_dict.append(temp)

    return list_dict

# print(cli(sys.argv))
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
input_mock.method.return_value = 'task_4.py 4 some_name=name some_address=address'

def test_return_type(monkeypatch):
    result = cli(input_mock.method().split())
    for elements in result:
        assert type(elements) is dict

def test_dict_content(monkeypatch):
    result = cli(input_mock.method().split())
    for elements in result:
        for value in elements.values():
            assert type(value) is str

