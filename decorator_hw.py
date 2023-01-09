import random


def get_random_value():
    return random.choice((1, 2, 3, 4, 5))


def get_random_values(choices, size=2):
    return random.choices(choices, k=size)


def retry(attempts=5, desired_value=None):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            current_attempt = 1
            while current_attempt <= attempts:
                result = func(*args, **kwargs)
                if result == desired_value:
                    print(result)
                    return result
                current_attempt += 1
            print('failure')
        return inner_wrapper
    return wrapper


@retry(desired_value=3)
def get_random_value():
    return random.choice((1, 2, 3, 4, 5))


@retry(desired_value=[1, 2])
def get_random_values(choices, size=2):
    return random.choices(choices, k=size)


get_random_value()
get_random_values([1, 2, 3, 4])
get_random_values([1, 2, 3, 4], 3)
get_random_values([1, 2, 3, 4], size=1)


@retry(attempts=7, desired_value=3)
def get_random_value():
    return random.choice((1, 2, 3, 4, 5))


@retry(attempts=2, desired_value=[1, 2, 3])
def get_random_values(choices, size=2):
    return random.choices(choices, k=size)


get_random_value()
get_random_values([1, 2, 3, 4])
get_random_values([1, 2, 3, 4], 3)
get_random_values([1, 2, 3, 4], size=1)

print("="*50)


def print_border(n):
    print(n*'*')


def print_middle(n, s):
    if n < 1:
        return
    print('*' + s*' ' + '*')
    print_middle(n-1, s)


def print_square(n):
    if n == 1:
        print('*')
        return
    if n == 2:
        print('**')
        print('**')
        return
    print_border(n)
    print_middle(n-2, n-2)
    print_border(n)


print_square(3)
