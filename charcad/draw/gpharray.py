# graphic object array


class GraphicObjectArray:
    def __init__(self):
        self._keys = list()
        self._vals = list()

    def __getitem__(self, item):
        return self._vals[item]
    
    def __len__(self):
        return len(self._keys)

    def __repr__(self):
        z = zip(self._keys, self._vals)
        return 'Graphic Object Array[\n    %s\n]' % ',\n    '.join([('%s: ' + k) % v for k, v in z])

    def add(self, obj):
        i = len(self._keys)
        name = 'object_{}'.format(i)
        self._keys.append(name)
        self._vals.append(obj)
