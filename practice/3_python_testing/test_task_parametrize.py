"""
Write a parametrized test for two functions.
The functions are used to find a number by ordinal in the Fibonacci sequence.
One of them has a bug.

Fibonacci sequence: https://en.wikipedia.org/wiki/Fibonacci_number

Task:
 1. Write a test with @pytest.mark.parametrize decorator.
 2. Find the buggy function and fix it.
"""
import pytest

fib_seq = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]


@pytest.mark.parametrize('n', [x for x in range(0, 13)])
def test_fib1(n):
    assert fibonacci_1(n) in fib_seq


@pytest.mark.parametrize('n', [x for x in range(0,13)])
def test_fib2(n):
    print(fibonacci_2(n))
    assert fibonacci_2(n) in fib_seq


def fibonacci_1(n):
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a + b
    return b


def fibonacci_2(n):
    fibo = [0, 1, 1]
    for i in range(2, n):
        fibo.append(fibo[-1] + fibo[-2])
    return fibo[n]


