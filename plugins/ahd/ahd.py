import os
import re

from settings import dictonary_path
from dictionary.base import Dictionary, Entry, lazy_property

re_dt = re.compile(r'[A-Z]{2,}')
re_filename = re.compile(r'^([0-9]{2}|roots)/[A-Z]+[0-9]+\.html$')
re_em = re.compile(r'<I>(.*?)</I>')


def repack_entry(filename):
    path = os.path.join(dictonary_path, filename)
    content = open(path)
    dl = []
    cnt = 0
    word = '?'
    for line in content:
        if cnt < 3:
            if cnt == 0:
                word = line.strip().split(':')[1]
            cnt += 1
            continue
        line = line.strip().replace('!!DICTIONARY!!', '#')
        line = re_em.sub(r'*\1*', line)
        if re_dt.match(line):
            dl.append(('dt', line))
        else:
            dl.append(('dd', line))
    return {
        'id': filename,
        'name': word,
        'content': dl,
    }


class AmericanHeritageDictionary(Dictionary):
    def load_index(self):
        with open('tmp/index.dat') as fh:
            for line in fh:
                (entry_id, name) = line.strip().split(':')
                entry = AmericanHeritageEntry(entry_id, name)
                self.items[name].append(entry)
                self.items_by_id[entry_id] = entry
        self.index = sorted(self.items)


class AmericanHeritageEntry(Entry):
    @lazy_property
    def content(self):
        return repack_entry(self.entry_id)


# All the HTML tags in the dictionary:
# 230802 <B>
#    1 <ENTRYWD>
#  286 <ETY Etyp="AETY">
#    3 <ETY Etyp="EMPTY">
#   18 <ETYREF>
#    5 <F>
# 24185 <FONT SIZE="+1">
# 12893 <FONT SIZE="-1">
# 25094 <FONT SIZE="-2">
#  116 <FR ALIGN = "C" STYLE = "S">
#    4 <FR SHAPE = "BUILT" ALIGN = "C" STYLE = "S">
#    1 <FR SHAPE = "CASE" ALIGN = "C" STYLE = "S">
#    5 <G>
# 173983 <I>
#    1 <INFEND>
#   47 <INREF>
#   31 <KW>
#    6 <NAME>
#    1 <RL>
#  340 <SC>
# 3718 <SUB>
# 36473 <SUP>
#    1 <TITLE>
# 1130 <b>
