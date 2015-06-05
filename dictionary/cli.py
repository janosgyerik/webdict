import abc
from argparse import ArgumentParser


class CommandLineInterface(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def get_and_print(self, entry_id):
        self.print_many(self.dictionary.get_entry(entry_id))

    def find_and_print(self, keyword, find_similar=False, list_only=False):
        self.print_many(self.dictionary.find(keyword, find_similar), list_only)

    def find_by_prefix_and_print(self, keyword, find_similar=False, list_only=False):
        self.print_many(self.dictionary.find_by_prefix(keyword, find_similar), list_only)

    def find_by_suffix_and_print(self, keyword, list_only=False):
        self.print_many(self.dictionary.find_by_suffix(keyword), list_only)

    def find_by_partial_and_print(self, keyword, list_only=False):
        self.print_many(self.dictionary.find_by_partial(keyword), list_only)

    def print_many(self, entries, list_only=False):
        for entry in entries:
            if list_only:
                print(entry.name)
            else:
                self.print_entry(entry)

    @abc.abstractmethod
    def print_entry(self, entry):
        pass

    def main(self):
        parser = ArgumentParser(
            description='Lookup words in {0}'.format(self.dictionary.name))
        parser.add_argument(
            '-b', '-s', '--prefix', action='store_true', default=False,
            help='find by prefix', )
        parser.add_argument(
            '-e', '--suffix', action='store_true', default=False,
            help='find by suffix', )
        parser.add_argument(
            '-p', '--partial', action='store_true', default=False,
            help='find partial match', )
        parser.add_argument(
            '-l', '--list', action='store_true', default=False,
            help='only list matches', )
        parser.add_argument(
            '--get', action='store_true', default=False,
            help='get entries by specified ids instead of word lookup', )
        parser.add_argument(
            '--similar', action='store_true', default=False,
            help='find similar words by shortening the prefix', )
        parser.add_argument('keywords', nargs='*',)
        args = parser.parse_args()

        if args.keywords:
            if args.get:
                for entry_id in args.keywords:
                    self.get_and_print(entry_id)
            elif args.prefix:
                for keyword in args.keywords:
                    self.find_by_prefix_and_print(keyword, find_similar=args.similar, list_only=args.list)
            elif args.suffix:
                for keyword in args.keywords:
                    self.find_by_suffix_and_print(keyword, list_only=args.list)
            elif args.partial:
                for keyword in args.keywords:
                    self.find_by_partial_and_print(keyword, list_only=args.list)
            else:
                for keyword in args.keywords:
                    self.find_and_print(keyword, find_similar=args.similar, list_only=args.list)
        else:
            parser.print_help()
