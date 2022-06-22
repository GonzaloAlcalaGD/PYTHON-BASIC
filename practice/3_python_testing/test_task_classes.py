"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""
import datetime

import pytest
import sys
sys.path.insert(1,'/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/2_python_part_2')
from task_classes import Homework, Teacher, Student


@pytest.fixture
def set_teacher():
    teacher = Teacher('Orlyakov', 'Dmitry')
    full_name = teacher.first_name+" "+teacher.last_name
    return full_name


@pytest.fixture
def set_student():
    student = Student('Vladislav', 'Popov')
    full_name = student.first_name+" "+student.last_name
    return full_name


@pytest.fixture
def set_homework():
    homework = Teacher.create_homework(self= None,text='create 2 simple classes', days=2)
    homework_task = homework.text
    return homework_task


@pytest.fixture
def set_negative_day_homework():
    homework = Teacher.create_homework(self=None,text='Learn Functions', days=-1)
    homework_days = homework.deadline
    return homework_days


# Test
def test_teacher(set_teacher):
    assert 'Dmitry Orlyakov' == set_teacher


def test_student(set_student):
    assert 'Popov Vladislav' == set_student


def test_homework(set_homework):
    assert 'create 2 simple classes' == set_homework


def test_negative_day_homework(set_negative_day_homework):
    set_day= datetime.datetime.now()
    assert set_negative_day_homework.day < set_day.day



