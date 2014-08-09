from dictionary.base import BaseDictionary, BaseEntry


class Dictionary(BaseDictionary):
    @property
    def name(self):
        return 'Dummy Dictionary'

    def load_index(self):
        self.add('hello')
        self.add('xhelloy')
        self.add('xhelloz')
        self.add('vanguard')
        self.add('sound', 4)
        for i in range(4):
            self.add(str(i) + 'sound')
        for i in range(14):
            self.add('knee' + str(i))
        self.reindex()

    def add(self, name, num=1):
        for _ in range(num):
            super(Dictionary, self).add(BaseEntry(name, name))
