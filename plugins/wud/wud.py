import os

from settings import dictionary_path
from dictionary.base import BaseDictionary, BaseEntry, lazy_property

INDEX_PATH = os.path.join(dictionary_path, 'index.dat')


def load_entry_content(word, filename):
    path = os.path.join(dictionary_path, filename)
    if not os.path.isfile(path):
        return
    with open(path) as fh:
        count = 0
        content = ''
        definition_list = []
        for line in fh:
            if count < 3:
                if count == 0:
                    word = line.strip().lower()
                count += 1
                continue
            line = line.strip()
            line = line.replace('*', '')
            if line:
                content += line + ' '
            else:
                definition_list.append(['', content])
                content = ''
        return {
            'id': filename,
            'name': word,
            'content': definition_list,
            'references': []
        }


class Dictionary(BaseDictionary):
    @property
    def name(self):
        return 'Webster\'s Unabridged Dictionary'

    @property
    def is_public(self):
        return True

    def load_index(self):
        with open(INDEX_PATH) as fh:
            for line in fh:
                (entry_id, name) = line.strip().split(':')
                entry = Entry(entry_id, name)
                self.add(entry)
        self.reindex()

    def get_entry(self, entry_id):
        entries = super(Dictionary, self).get_entry(entry_id)
        if not entries:
            entry = Entry(entry_id, '')
            if entry.content:
                entry.name = entry.content['name']
                self.add(entry)
                return [entry]
        return entries


class Entry(BaseEntry):
    @lazy_property
    def content(self):
        return load_entry_content(self.name, self.entry_id)
