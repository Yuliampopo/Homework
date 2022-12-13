def biggest(a, b):
    if a > b:
        return a
    else:
        return b


def smallest(a, b, c):
    if a < b and a < c:
        return a
    elif c < b and c < a:
        return c
    else:
        return b


def module(a):
    if a > 0:
        return a
    else:
        return -a


def summa(a, b):
    print(a + b)


def positive_number(a):
    if a > 0:
        print('positive number')
    elif a == 0:
        print('zero')
    else:
        print('negative number')
