from collections import defaultdict

import abc


class Entry(object):
    def __init__(self, entry_id, name, value=None):
        self.entry_id = entry_id
        self.name = name
        self.value = value

    def __repr__(self):
        return '%s: %s -> %s' % (self.entry_id, self.name, self.value)

    @abc.abstractmethod
    def get_value(self):
        """
        Load the actual Entry to represent the dictionary entry
        :return:
        """
        pass


class Match(object):
    def __init__(self, query, entry):
        self.query = query
        self.entry = entry

    def __repr__(self):
        return '%s: %s' % (self.query, self.entry)


class Dictionary(object):
    def __init__(self):
        self.index = {}
        self.items = defaultdict(list)
        self.items_by_id = {}
        self.load_index()
        # print('Loaded index with {} items'.format(len(self.index)))

    def find(self, word):
        matches = self.items.get(word)
        if matches:
            return [Match(word, x) for x in matches]
        return []

    def find_by_prefix(self, prefix):
        matches = []
        for k in self.index:
            if k.startswith(prefix):
                for entry in self.items[k]:
                    matches.append(Match(prefix, entry))
            elif matches:
                break
        return matches

    def find_by_suffix(self, suffix):
        matches = []
        for k in self.index:
            if k.endswith(suffix):
                for entry in self.items[k]:
                    matches.append(Match(suffix, entry))
        return matches

    def find_by_fragment(self, fragment):
        matches = []
        for k in self.index:
            if fragment in k:
                for entry in self.items[k]:
                    matches.append(Match(fragment, entry))
        return matches

    def get(self, entry_id):
        return self.items_by_id.get(entry_id)

    @abc.abstractmethod
    def load_index(self):
        """
        - Populate self.items with {word: [Entry, ...]}
        - Populate self.items_by_id with {id: Entry}
        - Populate self.index with {id: Entry}
        :return:
        """
        pass
