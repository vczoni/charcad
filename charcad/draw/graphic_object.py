

class GraphicObject:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class GraphicObjectArray:
    def __init__(self):
        self._objects = dict()

    def __getitem__(self, idx):
        k = self.keys
        k.sort()
        return self._objects[k[idx]]

    def __len__(self):
        return len(self._objects)

    def __repr__(self):
        z = zip(self.keys, self.values)
        return 'Graphic Object Array[\n    %s\n]' % \
            ',\n    '.join([(k + ': %s') % v for k, v in z])

    @property
    def keys(self):
        return [key for key in self._objects]

    @property
    def values(self):
        return [val for val in self._objects.values()]

    def add(self, obj):
        name = 'object_{:04d}'.format(self.__len__())
        self._objects.update({name: obj})

    def remove(self, key):
        del self._objects[key]

    def update(self, item):
        self._objects.update(item)
