import os
import re

from settings import dictionary_path
from dictionary.base import BaseDictionary, BaseEntry, lazy_property

INDEX_PATH = os.path.join(dictionary_path, 'index.dat')

re_strong_defs = re.compile(r'(Defn:|Syn\.)')
re_strong_numdots = re.compile(r'(\d+\. )')
re_strong_alphadots = re.compile(r'(\([a-z]\))')
re_em_roundbr = re.compile(r'(\([A-Z][a-z]+\.\))')
re_em_squarebr = re.compile(r'(\[[A-Z][a-z]+\.\])')


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
            line = re_strong_defs.sub(r'**\1**', line)
            line = re_strong_numdots.sub(r'**\1** ', line)
            line = re_strong_alphadots.sub(r'**\1**', line)
            line = re_em_roundbr.sub(r'*\1*', line)
            line = re_em_squarebr.sub(r'*\1*', line)

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

    @property
    def license(self):
        return """
        The content of this dictionary is for the use of anyone anywhere
        at no cost and with almost no restrictions whatsoever.
        You may copy it, give it away or re-use it under the terms of
        the Project Gutenberg License included online at www.gutenberg.net"""

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
