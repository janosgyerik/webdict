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
from plugins.wud.wud import Dictionary


LEFT_MARGIN = 2

re_no_em = re.compile(r'\*([^*]+)\*')
re_no_strong = re.compile(r'\*\*([^*]+)\*\*')

wrapper = textwrap.TextWrapper()
wrapper.initial_indent = wrapper.subsequent_indent = ' ' * LEFT_MARGIN

dictionary = Dictionary()


class WebstersUnabridgedDictionaryCLI(CommandLineInterface):
    def print_entry(self, entry):
        name = entry.name
        print(name)
        print('-' * len(name))

        for _, dd in entry.content['content']:
            self.print_dd(dd)
            print('')

    @staticmethod
    def print_dd(text):
        text = re_no_strong.sub(r'\1', text)
        text = re_no_em.sub(r'\1', text)
        for line in wrapper.wrap(text):
            print(line)


def main():
    WebstersUnabridgedDictionaryCLI(dictionary).main()

if __name__ == '__main__':
    main()
