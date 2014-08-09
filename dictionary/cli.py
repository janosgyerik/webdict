import abc
from optparse import OptionParser


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
        parser = OptionParser()
        parser.set_usage('%prog [options] word...')
        parser.add_option('-b', '-s', '--prefix', action='store_true',
                          help='find by prefix', default=False)
        parser.add_option('-e', '--suffix', action='store_true', default=False,
                          help='find by suffix', )
        parser.add_option('-p', '--partial', action='store_true', default=False,
                          help='find partial match', )
        parser.add_option('-l', '--list', action='store_true', default=False,
                          help='only list matches', )
        parser.add_option('--get', action='store_true', default=False,
                          help='get entries by specified ids instead of word lookup', )
        parser.add_option('--similar', action='store_true', default=False,
                          help='find similar words by shortening the prefix', )
        parser.set_description('Lookup words in {}'.format(self.dictionary.name))
        (options, args) = parser.parse_args()

        if args:
            if options.get:
                for entry_id in args:
                    self.get_and_print(entry_id)
            elif options.prefix:
                for keyword in args:
                    self.find_by_prefix_and_print(keyword, find_similar=options.similar, list_only=options.list)
            elif options.suffix:
                for keyword in args:
                    self.find_by_suffix_and_print(keyword, list_only=options.list)
            elif options.partial:
                for keyword in args:
                    self.find_by_partial_and_print(keyword, list_only=options.list)
            else:
                for keyword in args:
                    self.find_and_print(keyword, find_similar=options.similar, list_only=options.list)
        else:
            parser.print_help()
