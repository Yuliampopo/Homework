from dataclasses import dataclass
import json
import os

import pytest

from things_to_test_hw import search_in_file, add_from_json, Storage


@pytest.fixture
def file():
    lines = ['first_line\n', 'second_Line\n', 'third_line\n']
    file_name = 'file.txt'
    print("setup")
    with open(file_name, 'w') as file:
        file.writelines(lines)
    yield file_name
    os.remove(file_name)


def test_search_success(file):
    assert search_in_file(file, 'line') == ['first_line\n', 'third_line\n']


def test_search_no_file():
    with pytest.raises(FileNotFoundError):  # self.assertRaises(FileNotFoundError):
        search_in_file('not_found.txt', 'line')


def test_search_empty(file):
    assert search_in_file(file, 'pattern') == []


@pytest.fixture
def json_file():
    data = {'a': 3, 'b': 4, 'c': -1}
    file_name = 'file.json'
    with open(file_name, 'w') as file:
        json.dump(data, file)
    yield file_name
    os.remove(file_name)


def test_add_json_success(json_file):
    assert add_from_json(json_file, ('a', 'b', 'c')) == 6


def test_add_json_no_file():
    with pytest.raises(FileNotFoundError):
        add_from_json('not_found.json', ('a', 'b', 'c'))


def test_add_json_no_key(json_file):
    with pytest.raises(KeyError):
        add_from_json(json_file, ('a', 'b', 'd'))


@dataclass
class Customer:
    customer_id: int
    first_name: str
    last_name: str


@dataclass
class Account:
    account_id: int
    balance: float
    account_type: str
    owner_id: int


@pytest.fixture
def storage():
    test_storage = Storage()
    test_storage.add_table('customers', Customer)
    customer1 = Customer(1, 'John', 'Doe')
    customer2 = Customer(2, 'Foo', 'Bar')
    test_storage.add_to_table('customers', customer1, customer2)
    return test_storage


def test_add_table_success(storage):
    storage.add_table('accounts', Account)
    assert storage._data['accounts']['name'] == 'accounts'
    isinstance(storage._data['accounts']['structure'], Account)
    assert storage._data['accounts']['data'] == []


def test_add_table_failure(storage):
    with pytest.raises(ValueError):
        storage.add_table('customers', Customer)


def test_get_from_table_success(storage):
    assert storage.get_from_table('customers') == \
                     [
                        Customer(customer_id=1, first_name='John', last_name='Doe'),
                        Customer(customer_id=2, first_name='Foo', last_name='Bar')
                     ]


def test_get_from_table_failure(storage):
    with pytest.raises(ValueError):
        storage.get_from_table('no_such_table')


def test_add_to_table_success(storage):
    customer3 = Customer(3, 'Carl', 'Smith')
    storage.add_to_table('customers', customer3)
    assert storage.get_from_table('customers') == \
        [
            Customer(customer_id=1, first_name='John', last_name='Doe'),
            Customer(customer_id=2, first_name='Foo', last_name='Bar'),
            Customer(customer_id=3, first_name='Carl', last_name='Smith')
        ]


def test_add_to_table_failure(storage):
    account1 = Account(1, 123.45, 'Credit', 2)
    customer3 = Customer(3, 'Carl', 'Smith')
    with pytest.raises(ValueError):
        storage.add_to_table('wrong_table', customer3)
    with pytest.raises(ValueError):
        storage.add_to_table('customers', account1)
