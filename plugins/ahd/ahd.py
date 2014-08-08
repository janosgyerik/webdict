import os
import re

from settings import dictonary_path
from dictionary.base import Dictionary, Entry, lazy_property

re_dt = re.compile(r'[A-Z]{2,}')
re_filename = re.compile(r'^([0-9]{2}|roots)/[A-Z]+[0-9]+\.html$')
re_em = re.compile(r'<I>(.*?)</I>')
re_strong = re.compile(r'<[bB]>(.*?)</[bB]>')
re_other_html = re.compile(r'<[^>]+>')

#<A HREF="#?file=73/H0237300.html">hold<SUP><FONT SIZE="-1">1</FONT></SUP></A>
re_ref = re.compile(r'<A HREF="([^"]*)">(.*?)</A>')
re_word_index = re.compile(r'(\d+)$')

#<B>sound'ly</B> ---<FONT SIZE="-2">ADVERB</FONT><B>sound'ness</B> ---<FONT SIZE="-2">NOUN</FONT>
re_em_caps = re.compile(r'---<FONT SIZE="-2">([A-Z ]+)</FONT>')


def to_ref(raw_href, raw_word):
    word = re_other_html.sub('', raw_word)
    word = re_word_index.sub(r'-\1', word)
    ref = 'ref:{}:{}'.format(raw_href.replace('!!DICTIONARY!!?file=', ''), word)
    return ref, word


def repack_entry(filename):
    path = os.path.join(dictonary_path, filename)
    if not os.path.isfile(path):
        return
    with open(path) as fh:
        dl = []
        cnt = 0
        word = None
        dt = None
        refs = []
        for line in fh:
            if cnt < 3:
                if cnt == 0:
                    word = line.strip().split(':')[1]
                cnt += 1
                continue
            line = line.strip()
            for raw_href, raw_word in re_ref.findall(line):
                ref, ref_word = to_ref(raw_href, raw_word)
                if ref not in refs:
                    refs.append(ref)
                line = line.replace('<A HREF="{}">{}</A>'.format(raw_href, raw_word),
                                    '[{}][{}]'.format(ref_word, refs.index(ref) + 1))
            line = re_em.sub(r'*\1*', line)
            line = re_strong.sub(r'**\1**', line)
            line = re_em_caps.sub(r'---\1; ', line)
            line = re_other_html.sub('', line)
            if re_dt.match(line):
                dt = line
            else:
                dl.append([dt, line])
        if refs:
            dl.append(['REFERENCES', refs])
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
                self.add(entry)
        self.reindex()

    def get(self, entry_id):
        entries = super(AmericanHeritageDictionary, self).get(entry_id)
        if not entries:
            entry = AmericanHeritageEntry(entry_id, '')
            if entry.content:
                entry.name = entry.content['name']
                self.add(entry)
                return [entry]
        return entries


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
