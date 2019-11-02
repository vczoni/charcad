# canvas module

from charcad.draw.graph import GraphicObject, GraphicObjectArray, Graph
from charcad.draw.point import Point
from charcad.draw.line import Horizontal, Vertical
from charcad.draw.route import Route


class Canvas(GraphicObject):
    def __init__(self, w, h):
        super(Canvas, self).__init__()
        self.draw = Draw(self)
        self.w = w + 1
        self.h = h + 1
        self.reset()

    def reset(self):
        self.objects = GraphicObjectArray()
        self.reset_graph()

    def reset_graph(self):
        self.graph = Graph(w=self.w, h=self.h)

    # aux methods (A-Z)

    def add_object(self, obj, coord=None):
        if not coord is None:
            obj.set_coordinates(coord)
        self.objects.add(obj)

    def remove_object(self, key):
        self.objects.remove(key)

    def show(self, axes=False, frame=False):
        self.reset_graph()
        self.graph.add_objects(self.objects)
        self.graph.print(axes=axes, frame=frame)

    def undo(self):
        self.objects.remove(-1)


class Draw:
    def __init__(self, outer):
        self._canvas = outer
        self.line = Line(outer)

    def point(self, p):
        if isinstance(p, (list, tuple)):
            p = Point(*p)
        self._canvas.add_object(p)

    def route(self, *p, marker='.', origin_marker=None, transparent=True):
        if origin_marker is None:
            origin_marker = marker
        p = list(p)
        for i, item in enumerate(p):
            if isinstance(item, (tuple, list)):
                p[i] = Point(*item)
            elif isinstance(item, Point):
                p[i] = item
        route = Route(transparent=transparent)
        route.create_route(*p, marker=marker, origin_marker=origin_marker)
        self._canvas.add_object(route)


class Line:
    def __init__(self, outer):
        self._canvas = outer

    def __call__(self, direction, *a, **kw):
        if direction.lower() in ['h', 'horizontal']:
            self.horizontal(*a, **kw)
        elif direction.lower() in ['v', 'vertical']:
            self.vertical(*a, **kw)
        else:
            raise Exception(
                "'%s' is an invalid direction." % direction)

    def horizontal(self, x, y, length, marker=None):
        line = Horizontal(x, y, length, marker)
        self._canvas.add_object(line)

    def vertical(self, x, y, length, marker=None):
        line = Vertical(x, y, length, marker)
        self._canvas.add_object(line)
