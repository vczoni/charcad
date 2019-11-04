from charcad.draw.graph import Graph, GraphicObject, GraphicObjectArray
from charcad.draw.point import Point
from charcad.draw.coordinates import Coordinates


class Text(GraphicObject):
    def __init__(self, x=0, y=0, transparent=True, formatter=None, text=None):
        super(Text, self).__init__(x, y, transparent)
        self.formatter = formatter
        self.objects = GraphicObjectArray()
        if text is not None:
            self.write(text)

    @property
    def origin(self):
        self.coord = Coordinates(self.x, self.y)
        return self.coord

    def add_point(self, p):
        self.objects.add(p)

    def format_text(self):
        for obj in self.objects:
            obj.set_formatter(self.formatter)

    def update_graph(self, w=1, h=1):
        self.graph = Graph(w=w, h=h)
        for obj in self.objects:
            self.graph.add_graph(obj)

    def write(self, text):
        if isinstance(text, (list, tuple)):
            w = max([len(t) for t in text])
            h = len(text)
            self.set_y(self.y - (h-1))
            for j, txt in enumerate(text):
                j_ = (h-1) - j
                for i, t in enumerate(txt):
                    p = Point(i, j_, marker=t)
                    self.add_point(p)
        elif isinstance(text, str):
            w = len(text)
            h = 1
            for i, t in enumerate(text):
                p = Point(i, 0, marker=t)
                self.add_point(p)
        else:
            raise TypeError("'text' must be s string or a list of strings")
        self.format_text()
        self.update_graph(w, h)
