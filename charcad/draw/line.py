
from charcad.draw.coordinates import Coordinates
from charcad.draw.graph import GraphicObject, GraphicObjectArray, Graph
from charcad.draw.point import Point
from charcad.draw.utils import calc_angle, calc_distance, chrs as ch


class Line(GraphicObject):

    def __init__(self, x, y):
        super(Line, self).__init__(x, y)
        self.objects = GraphicObjectArray()

    def __repr__(self):
        return 'Line at <%s>' % id(self)

    def __len__(self):
        return len(self.objects)

    @property
    def origin(self):
        self.coord = Coordinates(self.x, self.y)
        return self.coord

    @property
    def end(self):
        x = self.objects[-1].coord.x
        y = self.objects[-1].coord.y
        self.coord = Coordinates(x, y)
        return self.coord

    @property
    def length(self):
        return len(self)

    def add_point(self, p):
        self.objects.add(p)

    def update_graph(self, w=1, h=1):
        self.graph = Graph(w=w, h=h)
        origin = self.origin
        for obj in self.objects:
            obj.coord -= origin
            self.graph.add_graph(obj)


class Horizontal(Line):
    def __init__(self, x, y, length, marker=None):
        super(Horizontal, self).__init__(x, y)
        if marker is None:
            marker = ch.lr
        self.marker = marker
        self.create(length)

    def create(self, length):
        for i in range(length):
            self.add_point(Point(self.x+i, self.y, marker=self.marker))
        self.update_graph(w=length)


class Vertical(Line):
    def __init__(self, x, y, length, marker=None):
        super(Vertical, self).__init__(x, y)
        if marker is None:
            marker = ch.ud
        self.marker = marker
        self.create(length)

    def create(self, length):
        for i in range(length):
            self.add_point(Point(self.x, self.y+i, marker=self.marker))
        self.update_graph(h=length)
