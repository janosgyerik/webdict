#!/usr/bin/env python

import re
import textwrap

try:
    from dictionary.cli import CommandLineInterface
except ImportError:
    from os.path import dirname, realpath
    from sys import path
    path.append(dirname(dirname(dirname(realpath(__file__)))))
    from dictionary.cli import CommandLineInterface
from plugins.ahd.ahd import AmericanHeritageDictionary


LEFT_MARGIN = 2

re_no_em = re.compile(r'\*([^*]+)\*')
re_no_strong = re.compile(r'\*\*([^*]+)\*\*')

wrapper = textwrap.TextWrapper()
wrapper.initial_indent = wrapper.subsequent_indent = ' ' * LEFT_MARGIN

dictionary = AmericanHeritageDictionary()


class AmericanHeritageDictionaryCLI(CommandLineInterface):
    @property
    def name(self):
        return 'The American Heritage Dictionary'

    def print_entry(self, entry):
        name = entry.name
        print(name)
        print('-' * len(name))

        dl_items = entry.content['content']
        dl = dict(dl_items)
        sections = [dt for dt, dd in dl_items if dt != 'REFERENCES']
        for dt in sections:
            print dt
            self.print_dd(dl[dt])
            print('')

    @staticmethod
    def print_dd(text):
        text = re_no_strong.sub(r'\1', text)
        text = re_no_em.sub(r'\1', text)
        for line in wrapper.wrap(text):
            print(line)


def main():
    AmericanHeritageDictionaryCLI(dictionary).main()

if __name__ == '__main__':
    main()
