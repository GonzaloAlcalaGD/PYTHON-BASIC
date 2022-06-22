"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import pytest
import tempfile



# Fixture


@pytest.fixture
def set_first_file():
    file = '/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/2_python_part_2/file1.txt'
    file1 = []
    with open(file, 'r') as f:
        file1 = f.read().split('\n')
    return file1


@pytest.fixture
def set_second_file():
    file = '/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/2_python_part_2/file2.txt'
    file2 = []
    with open(file, 'r') as f:
        file2 = f.read().split(',')
    return file2


# Tests

def test_first_file(set_first_file):
    print(set_first_file)
    assert set_first_file == ['osemkvq', 'gkk', 'bmqghimd', 'toiafxmy', 'dkqq', 'ibfdbtmims', 'veytyxwjx', 'voe', 'bxha', 'flsiqf', 'pnugfqtfv', 'tjmldhvunr', 'iyrlntskn', 'qchcg', 'pgrkde', 'vnfyu', 'wkexx', 'jvvwlfcpbu', 'ysgzjswszj', 'drgxroev']


def test_second_file(set_second_file):
    print(set_second_file)
    assert set_second_file == ['drgxroev', 'ysgzjswszj', 'jvvwlfcpbu', 'wkexx', 'vnfyu', 'pgrkde', 'qchcg', 'iyrlntskn', 'tjmldhvunr', 'pnugfqtfv', 'flsiqf', 'bxha', 'voe', 'veytyxwjx', 'ibfdbtmims', 'dkqq', 'toiafxmy', 'bmqghimd', 'gkk', 'osemkvq']

