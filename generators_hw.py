def get_even_or_odd_numbers(number, even):
    return list(filter(lambda n: n % 2 == (0 if even else 1), range(number + 1)))


def search_words(pattern, strings):
    return list(filter(lambda string: pattern in string, strings))


def flatten(list_with_sublists):
    yield from [item for sublist in list_with_sublists for item in sublist]


if __name__ == '__main__':
    assert get_even_or_odd_numbers(3, True) == [0, 2]
    assert get_even_or_odd_numbers(4, False) == [1, 3]

    assert search_words('he', ['hello', 'orange', 'phenomenon']) == ['hello', 'phenomenon']
    assert search_words('abc', ['hello', 'orange', 'phenomenon']) == []

    generator = flatten([[1, 2], [], [3, 4, 5]])
    assert next(generator) == 1
    assert next(generator) == 2
    assert next(generator) == 3
    assert next(generator) == 4
    assert next(generator) == 5