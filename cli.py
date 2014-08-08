#!/usr/bin/env python

import re
import textwrap

from optparse import OptionParser

from plugins.ahd.ahd import AmericanHeritageDictionary


LEFT_MARGIN = 2

re_no_em = re.compile(r'\*([^*]+)\*')
re_no_strong = re.compile(r'\*\*([^*]+)\*\*')

wrapper = textwrap.TextWrapper()
wrapper.initial_indent = wrapper.subsequent_indent = ' ' * LEFT_MARGIN

dictionary = AmericanHeritageDictionary()


def get_and_print(entry_id):
    print_many(dictionary.get(entry_id))


def find_and_print(keyword, find_similar=False, list_only=False):
    print_many(dictionary.find(keyword, find_similar), list_only)


def find_by_prefix_and_print(keyword, find_similar=False, list_only=False):
    print_many(dictionary.find_by_prefix(keyword, find_similar), list_only)


def find_by_suffix_and_print(keyword, list_only=False):
    print_many(dictionary.find_by_suffix(keyword), list_only)


def find_by_fragment_and_print(keyword, list_only=False):
    print_many(dictionary.find_by_fragment(keyword), list_only)


def print_many(entries, list_only=False):
    for entry in entries:
        if list_only:
            print(entry.name)
        else:
            print_entry(entry)


def print_entry(entry):
    name = entry.name
    print(name)
    print('-' * len(name))

    dl_items = entry.content['content']
    dl = dict(dl_items)
    sections = [dt for dt, dd in dl_items if dt != 'REFERENCES']
    for dt in sections:
        print dt
        print_dd(dl[dt])
        print('')


def print_dd(text):
    text = re_no_strong.sub(r'\1', text)
    text = re_no_em.sub(r'\1', text)
    for line in wrapper.wrap(text):
        print(line)


def main():
    parser = OptionParser()
    parser.set_usage('%prog [options] word...')
    parser.add_option('-b', '-s', '--prefix', action='store_true',
                      help='find by prefix', default=False)
    parser.add_option('-e', '--suffix', action='store_true', default=False,
                      help='find by suffix', )
    parser.add_option('-p', '--fragment', action='store_true', default=False,
                      help='find partial match', )
    parser.add_option('-l', '--list', action='store_true', default=False,
                      help='only list matches', )
    parser.add_option('--get', action='store_true', default=False,
                      help='get entries by specified ids instead of word lookup', )
    parser.add_option('--similar', action='store_true', default=False,
                      help='find similar words by shortening the prefix', )
    parser.set_description('Lookup words in the American Heritage Dictionary')
    (options, args) = parser.parse_args()

    if args:
        if options.get:
            for entry_id in args:
                get_and_print(entry_id)
        elif options.prefix:
            for keyword in args:
                find_by_prefix_and_print(keyword, find_similar=options.similar, list_only=options.list)
        elif options.suffix:
            for keyword in args:
                find_by_suffix_and_print(keyword, list_only=options.list)
        elif options.fragment:
            for keyword in args:
                find_by_fragment_and_print(keyword, list_only=options.list)
        else:
            for keyword in args:
                find_and_print(keyword, find_similar=options.similar, list_only=options.list)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
