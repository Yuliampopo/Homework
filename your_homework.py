import os
import sys


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


if __name__ == '__main__':
    try:
        a, b = sys.argv[1:]

        result = {
            'add': add,
            'subtract': subtract,
            'multiply': multiply,
            'divide': divide,
        }[os.environ.get('FUNCTION', 'add')](int(a), int(b))

        print(result)
    except ValueError as e:
        print(e)
        exit(2)
    except KeyError as e:
        print('Wrong function:', e)
        exit(2)
