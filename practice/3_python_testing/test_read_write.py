"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import tempfile
import pytest


# Fixture
@pytest.fixture
def set_path():
    file = '/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/2_python_part_2/files/result.txt'
    return file


@pytest.fixture
def get_file(set_path):
    result = []
    with open(set_path, 'r') as i:
        result.append(i.read())
    return [x for xs in result for x in xs.split(',')]


@pytest.fixture
def set_result():
    expected = ['80', '37', '15']
    return expected

# Tests


def test_compare_files(get_file, set_result):
    assert get_file == set_result




