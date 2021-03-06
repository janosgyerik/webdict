#!/usr/bin/env python

import unittest
from test.test_support import run_unittest

from wud import Dictionary


test_dict = Dictionary()


class TestSearchResultCounts(unittest.TestCase):
    def setUp(self):
        self.dict = test_dict

    def assert_matched_count(self, count, results):
        self.assertEqual(count, len(results))

    def test_find_none(self):
        self.assert_matched_count(0, self.dict.find("nonexistentx"))

    def test_find_by_exact_single(self):
        self.assert_matched_count(1, self.dict.find("hello"))

    def test_find_by_exact_many(self):
        self.assert_matched_count(11, self.dict.find("sound"))

    def test_find_by_prefix_none(self):
        self.assert_matched_count(0, self.dict.find_by_prefix("kneex"))

    def test_find_by_prefix_single(self):
        self.assert_matched_count(1, self.dict.find_by_prefix("hello"))

    def test_find_by_prefix_many(self):
        self.assert_matched_count(16, self.dict.find_by_prefix("knee"))

    def test_find_by_suffix_none(self):
        self.assert_matched_count(0, self.dict.find_by_suffix("kneex"))

    def test_find_by_suffix_single(self):
        self.assert_matched_count(1, self.dict.find_by_suffix("hello"))

    def test_find_by_suffix_many(self):
        self.assert_matched_count(19, self.dict.find_by_suffix("sound"))

    def test_find_by_partial_none(self):
        self.assert_matched_count(0, self.dict.find_by_partial("kneex"))

    def test_find_by_partial_single(self):
        self.assert_matched_count(1, self.dict.find_by_partial("vanguard"))

    def test_find_by_partial_many(self):
        self.assert_matched_count(4, self.dict.find_by_partial("hello"))


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
                'id': 'l/lo/lo_/lo_-60016.txt',
                'name': 'lo',
                'content': [['', 'Lo, interj. Etym: [OE. lo, low; perh. akin to E. look, v.]'],
                            ['',
                             '**Defn:** Look; see; behold; observe. " Lo, '
                             'here is Christ." Matt. xxiv. **23. ** " Lo, '
                             'we turn to the Gentiles." Acts xiii. 46.']],
                'references': []
            }, entry.content)

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
        entry = self.dict.find('behold')[1]
        self.assertEqual(
            {
                'content': [['', 'Behold", v. i.'],
                            ['', '**Defn:** To direct the eyes to, '
                                 'or fix them upon, an object; to look; '
                                 'to see. And I beheld, and, lo, in the '
                                 'midst of the throne, . . . a lamb as it '
                                 'had been slain. Rev. v. 6.']],
                'references': [],
                'id': 'b/be/beh/behold-9941.txt',
                'name': 'behold-2'
            },
            entry.content
        )

    def test_cross_references_multiple(self):
        entry = self.dict.find('sound')[1]
        self.assertEqual(
            {
                'content': [['', 'Sound, n. (Zo\xc3\xb6l.)'],
                            ['', '**Defn:** A cuttlefish. *[Obs.]* Ainsworth.']],
                'references': [],
                'id': 's/so/sou/sound-97349.txt',
                'name': 'sound-2'
            },
            entry.content
        )


def test_main():
    run_unittest(
        TestSearchResultCounts,
        TestSearchOutput
    )


if __name__ == '__main__':
    test_main()
