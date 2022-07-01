from multiprocessing import Pool
import os
from random import randint
import timeit
import csv


OUTPUT_DIR = '/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/7_concurrency/output/'
RESULT_FILE = '/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/7_concurrency/output/result.csv'
func1_store_results = []

def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""
    f0, f1 = 0, 1
    for _ in range(n-1):
        f0, f1 = f1, f0 + f1
    return f1
    
def func1(array: list):
    """
    Calculates fibonacci numbers from a list of ordinal numbers
    """
    return fib(array)


def write_func1(result_file: list, filenames: list):
    """
    Writes files from a list of ordinal numbers and their fibonacci numbers
    """
    for index in range(len(result_file)):
        with open(OUTPUT_DIR+str(filenames[index])+'.txt', 'w') as f:
            f.write(str(result_file[index]))


def func2(result_file: str):
    with open(result_file, 'w') as w:
        for filename in os.listdir(OUTPUT_DIR):
            with open(OUTPUT_DIR+filename, 'r') as f:
                writer = csv.writer(w)
                writer.writerow([filename[:-4], f.read()])
            


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
   
    # Create pool of workers
    pool = Pool()

    # Start the timer
    start = timeit.default_timer()
    # Create a list of random numbers
    array = [randint(1000, 100000) for _ in range(1000)]
    # Call the function func1 with the list of random numbers into multiprocessing
    f1 = pool.map(func1, array)
    # Write files
    write_func1(f1, array)
    # Stop the timer
    pool.close()
    func2(result_file=RESULT_FILE)
    end = timeit.default_timer()
    print(end-start)
    # print(end-start)