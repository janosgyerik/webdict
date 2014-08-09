from dictionary.base import Dictionary, Entry


class DummyDictionary(Dictionary):
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
            super(DummyDictionary, self).add(Entry(name, name))
