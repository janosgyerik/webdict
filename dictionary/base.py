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


class BaseEntry(object):
    def __init__(self, entry_id, name):
        self.entry_id = entry_id
        self.name = name

    @property
    def content(self):
        return {
            'id': self.entry_id,
            'name': self.name,
            'content': [],
            'references': [],
        }

    def __repr__(self):
        return '{0.__name__}({1.entry_id}, {1.name})'.format(type(self), self)


class BaseDictionary(object):
    @abc.abstractproperty
    def name(self):
        return '<The Dictionary>'

    @abc.abstractproperty
    def is_public(self):
        return False

    @property
    def license(self):
        return None

    def __init__(self):
        self.items_sorted = {}
        self.items_by_name = defaultdict(list)
        self.items_by_id = {}
        self.load_index()

    def find(self, word, find_similar=False):
        matches = self.items_by_name.get(word)
        if matches:
            return matches
        if find_similar:
            return self.find_by_prefix(word, find_similar=True)
        return []

    def find_by_prefix(self, prefix, find_similar=False):
        matches = []
        for k in self.items_sorted:
            if k.startswith(prefix):
                matches.extend(self.items_by_name[k])
            elif matches:
                break
        if find_similar and not matches and len(prefix) > 1:
            return self.find_by_prefix(prefix[:-1], find_similar=True)
        return matches

    def find_by_suffix(self, suffix):
        matches = []
        for k in self.items_sorted:
            if k.endswith(suffix):
                matches.extend(self.items_by_name[k])
        return matches

    def find_by_partial(self, partial):
        matches = []
        for k in self.items_sorted:
            if partial in k:
                matches.extend(self.items_by_name[k])
        return matches

    def get_entry(self, entry_id):
        entry = self.items_by_id.get(entry_id)
        if entry:
            return [entry]
        else:
            return []

    def add(self, entry):
        self.items_by_name[entry.name].append(entry)
        self.items_by_id[entry.entry_id] = entry

    def reindex(self):
        self.items_sorted = sorted(self.items_by_name)

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
