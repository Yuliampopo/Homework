from dataclasses import dataclass
import json
import os
import unittest

from things_to_test_hw import search_in_file, add_from_json, Storage


class TestSearchInFile(unittest.TestCase):

    def setUp(self):
        lines = ['first_line\n', 'second_Line\n', 'third_line\n']
        self.file_name = 'file.txt'
        with open(self.file_name, 'w') as file:
            file.writelines(lines)

    def tearDown(self):
        os.remove(self.file_name)

    def test_search_success(self):
        self.assertEqual(search_in_file(self.file_name, 'line'), ['first_line\n', 'third_line\n'])

    def test_search_no_file(self):
        with self.assertRaises(FileNotFoundError):
            search_in_file('not_found.txt', 'line')

    def test_search_empty(self):
        self.assertEqual(search_in_file(self.file_name, 'pattern'), [])


class TestAddJson(unittest.TestCase):

    def setUp(self):
        data = {'a': 3, 'b': 4, 'c': -1}
        self.file_name = 'file.json'
        with open(self.file_name, 'w') as file:
            json.dump(data, file)

    def tearDown(self):
        os.remove(self.file_name)

    def test_add_json_success(self):
        self.assertEqual(add_from_json(self.file_name, ('a', 'b', 'c')), 6)

    def test_add_json_no_file(self):
        with self.assertRaises(FileNotFoundError):
            add_from_json('not_found.json', ('a', 'b', 'c'))

    def test_add_json_no_key(self):
        with self.assertRaises(KeyError):
            add_from_json(self.file_name, ('a', 'b', 'd'))


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


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.storage = Storage()
        self.storage.add_table('customers', Customer)
        customer1 = Customer(1, 'John', 'Doe')
        customer2 = Customer(2, 'Foo', 'Bar')
        self.storage.add_to_table('customers', customer1, customer2)

    def test_add_table_success(self):
        self.storage.add_table('accounts', Account)
        self.assertEqual(self.storage._data['accounts']['name'], 'accounts')
        self.assertIs(self.storage._data['accounts']['structure'], Account)
        self.assertEqual(self.storage._data['accounts']['data'], [])

    def test_add_table_failure(self):
        with self.assertRaises(ValueError):
            self.storage.add_table('customers', Customer)

    def test_get_from_table_success(self):
        self.assertEqual(self.storage.get_from_table('customers'),
                         [
                            Customer(customer_id=1, first_name='John', last_name='Doe'),
                            Customer(customer_id=2, first_name='Foo', last_name='Bar')
                         ])

    def test_get_from_table_failure(self):
        with self.assertRaises(ValueError):
            self.storage.get_from_table('no_such_table')

    def test_add_to_table_success(self):
        customer3 = Customer(3, 'Carl', 'Smith')
        self.storage.add_to_table('customers', customer3)
        self.assertEqual(self.storage.get_from_table('customers'),
                         [
                             Customer(customer_id=1, first_name='John', last_name='Doe'),
                             Customer(customer_id=2, first_name='Foo', last_name='Bar'),
                             Customer(customer_id=3, first_name='Carl', last_name='Smith')
                         ])

    def test_add_to_table_failure(self):
        account1 = Account(1, 123.45, 'Credit', 2)
        customer3 = Customer(3, 'Carl', 'Smith')
        with self.assertRaises(ValueError):
            self.storage.add_to_table('wrong_table', customer3)
        with self.assertRaises(ValueError):
            self.storage.add_to_table('customers', account1)
