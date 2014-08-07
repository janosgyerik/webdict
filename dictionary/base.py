from collections import defaultdict

import abc


def lazy_property(fn):
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return _lazy_property


class Entry(object):
    def __init__(self, entry_id, name):
        self.entry_id = entry_id
        self.name = name

    @abc.abstractmethod
    def content(self):
        pass

    def __repr__(self):
        return '%s: %s' % (self.entry_id, self.name)


class Dictionary(object):
    def __init__(self):
        self.index = {}
        self.items = defaultdict(list)
        self.items_by_id = {}
        self.load_index()
        # print('Loaded index with {} items'.format(len(self.index)))

    def find(self, word, find_similar=False):
        matches = self.items.get(word)
        if matches:
            return matches
        if find_similar:
            return self.find_by_prefix(word, find_similar=True)
        return []

    def find_by_prefix(self, prefix, find_similar=False):
        matches = []
        for k in self.index:
            if k.startswith(prefix):
                matches.extend(self.items[k])
            elif matches:
                break
        if find_similar and not matches and len(prefix) > 1:
            return self.find_by_prefix(prefix[:-1], find_similar=True)
        return matches

    def find_by_suffix(self, suffix):
        matches = []
        for k in self.index:
            if k.endswith(suffix):
                matches.extend(self.items[k])
        return matches

    def find_by_fragment(self, fragment):
        matches = []
        for k in self.index:
            if fragment in k:
                matches.extend(self.items[k])
        return matches

    def get(self, entry_id):
        return self.items_by_id.get(entry_id)

    def add(self, entry):
        self.items[entry.name].append(entry)
        self.items_by_id[entry.entry_id] = entry

    def reindex(self):
        self.index = sorted(self.items)

    @abc.abstractmethod
    def load_index(self):
        """
        Populate the index. Implement like this:
            for entry in entries:
                self.add(entry)
            self.reindex()
        :return:
        """
        pass
