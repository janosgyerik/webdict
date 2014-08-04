#!/usr/bin/env python

import unittest
from test.test_support import run_unittest

from ahd import AmericanHeritage

test_dict = AmericanHeritage()


class AmericanHeritageDictionaryTestCase(unittest.TestCase):

    def setUp(self):
        self.dict = test_dict

    def find(self, word):
        return self.dict.lookup(word)

    def assert_matched_count(self, count, word):
        self.assertEqual(count, len(self.find(word)))

    def test_find_none(self):
        self.assert_matched_count(0, "nonexistent")

    def test_find_by_exact_single(self):
        self.assert_matched_count(0, "nonexistent")

    def test_sanity(self):
        #TODO
        print(self.dict.lookup('sound'))
        print(self.dict.lookup('soundx'))
        print(self.dict.lookup_by_prefix('knee'))
        print(self.dict.lookup_by_suffix('sound'))
        print(self.dict.lookup_by_fragment('hello'))
        for item in self.dict.lookup('sound'):
            print(item)
        print(self.dict.lookup('hello'))

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
    run_unittest(AmericanHeritageDictionaryTestCase)

if __name__ == '__main__':
    test_main()
