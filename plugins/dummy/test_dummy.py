#!/usr/bin/env python

import unittest
from test.test_support import run_unittest

from dummy import Dictionary


test_dict = Dictionary()


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

    def test_find_by_partial_none(self):
        self.assert_matched_count(0, self.dict.find_by_partial("kneex"))

    def test_find_by_partial_single(self):
        self.assert_matched_count(1, self.dict.find_by_partial("vanguard"))

    def test_find_by_partial_many(self):
        self.assert_matched_count(3, self.dict.find_by_partial("hello"))


def test_main():
    run_unittest(DictionaryTestCase)


if __name__ == '__main__':
    test_main()
