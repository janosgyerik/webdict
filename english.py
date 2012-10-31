#!/usr/bin/env python

from optparse import OptionParser
import os
import re

from settings import dictonary_path
index_path = os.path.join(dictonary_path, 'index.dat')

re_dt = re.compile('[A-Z]{2,}')
re_filename = re.compile('^([0-9]{2}|roots)/[A-Z]+[0-9]+\.html$')

MIN_SIMILAR = 3
MIN_TERM_LENGTH = 4


def repack_entry(filename):
    path = os.path.join(dictonary_path, filename)
    content = open(path)
    dl = []
    cnt = 0
    word = '?'
    for line in content.readlines():
        if cnt < 3:
            if cnt == 0:
                word = line.strip().split(':')[1]
            cnt += 1
            continue
        line = line.strip().replace('!!DICTIONARY!!', '#')
        if re_dt.match(line):
            dl.append(('dt', line))
        else:
            dl.append(('dd', line))
    return {
            'word': word,
            'filename': filename,
            'dl': dl,
            }


def find(term):
    index_file = open(index_path)
    for entry in index_file.readlines():
        if entry.endswith(':' + term + '\n'):
            filename = entry.strip().split(':')[0]
            yield repack_entry(filename)


def find_similar(term):
    index_file = open(index_path)
    matches = []
    for entry in index_file.readlines():
        entry = entry.strip()
        (filename, word) = entry.split(':')
        if word.startswith(term):
            matches.append((filename, word))
    return matches


def similar(term0):
    term = term0
    results = []
    while True:
        results = find_similar(term)
        if len(results) > MIN_SIMILAR:
            break
        if len(term) > MIN_TERM_LENGTH:
            term = term[:len(term)-1]
        else:
            break
    return results


def get(filename):
    if re_filename.match(filename):
        return repack_entry(filename)
    return {}


def print_entry(entry):
    print entry


if __name__ == '__main__':
    parser = OptionParser()
    parser.set_usage('%prog [options] word...')
    parser.add_option('-b', '-s', '--start', action='store_true',
            help='find by start', default=False)
    parser.add_option('-e', '--end', action='store_true', default=False,
            help='find by end',)
    parser.add_option('-p', '--partial', action='store_true', default=False,
            help='find partial match',)
    parser.add_option('-l', '--list', action='store_true', default=False,
            help='only list matches',)
    parser.add_option('--get', action='store_true', default=False,
            help='get specified filenames instead of word lookup',)
    parser.add_option('--similar', action='store_true', default=False,
            help='find similar words by shortening the prefix',)
    parser.set_description('Lookup words in the American Heritage Dictionary')
    (options, args) = parser.parse_args()

    if args:
        if options.get:
            for filename in args:
                print_entry(get(filename))
        elif options.similar:
            for term in args:
                for result in similar(term):
                    print result
        else:
            for term in args:
                for entry in find(term):
                    print_entry(entry)
    else:
        parser.print_help()

# eof
