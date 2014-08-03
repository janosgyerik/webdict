#!/usr/bin/env python

import unittest
from test.test_support import run_unittest

from base import Dictionary


class DictionaryTestCase(unittest.TestCase):

    def setUp(self):
        class DummyDictionary(Dictionary):
            def load_index(self):
                pass

        self.dict = DummyDictionary()

    def find(self, word):
        return self.dict.lookup(word)

    def assert_matched_count(self, count, word):
        self.assertEqual(count, len(self.find(word)))

    def test_find_none(self):
        self.assert_matched_count(0, "nonexistent")

    def test_find_by_exact_single(self):
        self.dict.put('hello', 'greeting')
        self.assert_matched_count(0, "nonexistent")

    def test_find_by_exact_many(self):
        pass

    def test_find_by_prefix_none(self):
        pass

    def test_find_by_prefix_single(self):
        pass

    def test_find_by_prefix_many(self):
        pass

    def test_find_by_suffix_none(self):
        pass

    def test_find_by_suffix_single(self):
        pass

    def test_find_by_suffix_many(self):
        pass

    def test_find_by_fragment_none(self):
        pass

    def test_find_by_fragment_single(self):
        pass

    def test_find_by_fragment_many(self):
        pass


def test_main():
    run_unittest(DictionaryTestCase)

if __name__ == '__main__':
    test_main()
