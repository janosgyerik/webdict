#!/usr/bin/env python

import unittest
from test.test_support import run_unittest

from ahd import Dictionary


test_dict = Dictionary()


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

    def get_entry_n(self, word, n):
        return dict(self.dict.find(word)[n].content['content'])

    def get_first_entry(self, word):
        return self.get_entry_n(word, 0)

    def test_lo(self):
        entry = self.dict.find('lo')[0]
        self.assertEqual(
            {
                'id': '48/L0214800.html',
                'name': 'lo',
                'content': [['INTERJECTION',
                             'Used to attract attention or to show surprise.'],
                            ['ETYMOLOGY',
                             'Middle English, from Old English *la*.']]
            }, entry.content)

    def test_behold_verb(self):
        entry = self.get_first_entry('behold')
        self.assertEqual(
            "Inflected forms: **be-held** (-held'), **be-hold-ing**, **be-holds**",
            entry['VERB']
        )

    def test_indignation_name(self):
        word = 'indignation'
        self.assertEqual(
            word,
            self.dict.find(word)[0].name
        )
        self.assertEqual(
            word,
            self.dict.find(word)[0].content['name']
        )

    def test_cross_references(self):
        entry = self.get_first_entry('behold')
        self.assertEqual(
            "Middle English *biholden*, from Old English *behaldan* : *be-*, be- + *healdan*, to hold; see [hold-1][2].",
            entry['ETYMOLOGY']
        )
        self.assertEqual(
            ['ref:33/S0213300.html:see-1', 'ref:73/H0237300.html:hold-1'],
            entry['REFERENCES']
        )

    def test_cross_references_multiple(self):
        entry = self.get_entry_n('sound', 1)
        self.assertEqual(
            "**sound\'ly** ---ADVERB; **sound\'ness** ---NOUN; ",
            entry['OTHER FORMS']
        )
        self.assertEqual(
            ['ref:65/H0106500.html:healthy', 'ref:25/V0012500.html:valid'],
            entry['REFERENCES']
        )


def test_main():
    run_unittest(
        TestSearchResultCounts,
        TestSearchOutput
    )


if __name__ == '__main__':
    test_main()
