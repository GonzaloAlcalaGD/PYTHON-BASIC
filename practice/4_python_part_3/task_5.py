"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     #>>> make_request('https://www.google.com')
     200, 'response data'
"""
from typing import Tuple
import urllib.request
from unittest.mock import Mock, patch
import pytest


def make_request(url: str):
    code = urllib.request.urlopen(url).getcode()
    req = urllib.request.urlopen(url)
    charset = req.headers.get_content_charset()
    print(charset)
    response = req.read().decode(charset)
    return code, response


# print(make_request('https://www.google.com'))

"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""

c, r = make_request('https://www.google.com')
request = Mock()
request.method.return_value = 200


def test_request():
    code, response = make_request('https://www.google.com')
    request.method2.return_value = response
    assert code == request.method() and response == request.method2()