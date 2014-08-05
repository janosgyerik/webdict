#!/usr/bin/env python

import unittest
from test.test_support import run_unittest

from ahd import AmericanHeritageDictionary


test_dict = AmericanHeritageDictionary()


class TestSearchResultCounts(unittest.TestCase):
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


class TestSearchOutput(unittest.TestCase):
    def setUp(self):
        self.dict = test_dict

    def test_lo(self):
        # TODO this is not strict markdown: see the <I>la</I>
        entry = self.dict.find('lo')[0]
        self.assertEqual(
            {
                'id': '48/L0214800.html',
                'name': 'lo',
                'content': [('dt', 'INTERJECTION'),
                            ('dd',
                             'Used to attract attention or to show surprise.'),
                            ('dt', 'ETYMOLOGY'),
                            ('dd',
                             'Middle English, from Old English <I>la</I>.')]
            }, entry.content)

    def test_cross_references(self):
        pass


def test_main():
    run_unittest(
        TestSearchResultCounts,
        TestSearchOutput
    )


if __name__ == '__main__':
    test_main()
