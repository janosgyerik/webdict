from collections import defaultdict


class Entry(object):
    def __init__(self, entry_id, name, value=None):
        self.entry_id = entry_id
        self.name = name
        self.value = value

    def __repr__(self):
        return '%s: %s -> %s' % (self.entry_id, self.name, self.value)

    def load_value(self):
        pass


class Match(object):
    def __init__(self, query, entry, list_only=True):
        self.query = query
        self.entry = entry
        if not list_only:
            self.entry.load_value()

    def __repr__(self):
        return '%s: %s' % (self.query, self.entry)


class Dictionary(object):
    def __init__(self):
        self.index = []
        self.items = defaultdict(list)
        self.items_by_id = {}
        self.load_index()
        print('Loaded index with {} items'.format(len(self.index)))

    def lookup(self, word, list_only=True):
        matches = self.items.get(word)
        if matches:
            return [Match(word, x, list_only) for x in matches]
        return []

    def lookup_by_prefix(self, prefix, list_only=True):
        matches = []
        for k in self.index:
            if k.startswith(prefix):
                for entry in self.items[k]:
                    matches.append(Match(prefix, entry, list_only))
            elif matches:
                break
        return matches

    def lookup_by_suffix(self, suffix, list_only=True):
        matches = []
        for k in self.index:
            if k.endswith(suffix):
                for entry in self.items[k]:
                    matches.append(Match(suffix, entry, list_only))
        return matches

    def lookup_by_fragment(self, fragment, list_only=True):
        matches = []
        for k in self.index:
            if fragment in k:
                for entry in self.items[k]:
                    matches.append(Match(fragment, entry, list_only))
        return matches

    def get(self, entry_id):
        return self.items_by_id.get(entry_id)

    def load_index(self):
        pass
