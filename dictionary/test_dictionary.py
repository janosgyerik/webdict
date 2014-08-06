#!/usr/bin/env python

import unittest
from test.test_support import run_unittest

from base import Dictionary


class DummyDictionary(Dictionary):
    def load_index(self):
        pass

    def put(self, word, values=('dummy',)):
        self.items[word] = values
        self.index = sorted(self.items)


test_dict = DummyDictionary()
test_dict.put('hello')
test_dict.put('xhelloy')
test_dict.put('xhelloz')
test_dict.put('vanguard')
test_dict.put('sound', ['x' for _ in range(4)])
for i in range(4):
    test_dict.put(str(i) + 'sound')
for i in range(14):
    test_dict.put('knee' + str(i))


class DictionaryTestCase(unittest.TestCase):
    def setUp(self):
        self.dict = test_dict

    def assert_matched_count(self, count, results):
        self.assertEqual(count, len(results))

    def test_find_none(self):
        self.assert_matched_count(0, self.dict.find("nonexistent"))

    def test_find_by_exact_single(self):
        self.assert_matched_count(1, self.dict.find("hello"))

    def test_find_by_exact_many(self):
        self.assert_matched_count(4, self.dict.find("sound"))

    def test_find_by_prefix_none(self):
        self.assert_matched_count(0, self.dict.find_by_prefix("kneex"))

    def test_find_by_prefix_single(self):
        self.assert_matched_count(1, self.dict.find_by_prefix("hello"))

    def test_find_by_prefix_many(self):
        self.assert_matched_count(14, self.dict.find_by_prefix("knee"))

    def test_find_by_suffix_none(self):
        self.assert_matched_count(0, self.dict.find_by_suffix("kneex"))

    def test_find_by_suffix_single(self):
        self.assert_matched_count(1, self.dict.find_by_suffix("hello"))

    def test_find_by_suffix_many(self):
        self.assert_matched_count(8, self.dict.find_by_suffix("sound"))

    def test_find_by_fragment_none(self):
        self.assert_matched_count(0, self.dict.find_by_fragment("kneex"))

    def test_find_by_fragment_single(self):
        self.assert_matched_count(1, self.dict.find_by_fragment("vanguard"))

    def test_find_by_fragment_many(self):
        self.assert_matched_count(3, self.dict.find_by_fragment("hello"))


def test_main():
    run_unittest(DictionaryTestCase)


if __name__ == '__main__':
    test_main()
