import os
import re

from settings import dictonary_path
from dictionary.dictionary import Dictionary, Entry

re_dt = re.compile('[A-Z]{2,}')
re_filename = re.compile('^([0-9]{2}|roots)/[A-Z]+[0-9]+\.html$')


def repack_entry(filename):
    path = os.path.join(dictonary_path, filename)
    content = open(path)
    dl = []
    cnt = 0
    word = '?'
    for line in content.readlines():
        if cnt < 3:
            if cnt == 0:
                word = line.strip().split(':')[1]
            cnt += 1
            continue
        line = line.strip().replace('!!DICTIONARY!!', '#')
        if re_dt.match(line):
            dl.append(('dt', line))
        else:
            dl.append(('dd', line))
    return {
        'word': word,
        'filename': filename,
        'dl': dl,
    }


class AmericanHeritage(Dictionary):
    def load_index(self):
        with open('tmp/index.dat') as fh:
            for line in fh:
                (entry_id, name) = line.strip().split(':')
                entry = AmericanHeritageEntry(entry_id, name)
                self.items[name].append(entry)
                self.items_by_id[entry_id] = entry
        self.index = sorted(self.items)


class AmericanHeritageEntry(Entry):
    def load_value(self):
        self.value = repack_entry(self.entry_id)


dictionary = AmericanHeritage()
print(dictionary.lookup('sound'))
print(dictionary.lookup('soundx'))
print(dictionary.lookup_by_prefix('knee'))
print(dictionary.lookup_by_suffix('sound'))
print(dictionary.lookup_by_fragment('hello'))
for item in dictionary.lookup('sound'):
    print(item)
print(dictionary.lookup('hello'))
