#!/usr/bin/env python

try:
    from dictionary.cli import CommandLineInterface
except ImportError:
    from os.path import dirname, realpath
    from sys import path
    path.append(dirname(dirname(dirname(realpath(__file__)))))
    from dictionary.cli import CommandLineInterface

from plugins.dummy.dummy import Dictionary

dictionary = Dictionary()


class DummyDictionaryCLI(CommandLineInterface):
    def print_entry(self, entry):
        print(entry)


def main():
    DummyDictionaryCLI(dictionary).main()

if __name__ == '__main__':
    main()
