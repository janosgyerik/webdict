#!/usr/bin/env python

from dictionary.cli import CommandLineInterface
from plugins.dummy.dummy import DummyDictionary

dictionary = DummyDictionary()


class DummyDictionaryCLI(CommandLineInterface):
    @property
    def name(self):
        return 'Dummy Dictionary'

    def print_entry(self, entry):
        print(entry)


def main():
    DummyDictionaryCLI(dictionary).main()

if __name__ == '__main__':
    main()
