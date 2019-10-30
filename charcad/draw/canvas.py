# canvas module

from charcad.draw.graphic_object import GraphicObject, GraphicObjectArray, Graph
from charcad.draw.basic_geom import Point
from charcad.draw.route import Route


class Canvas(GraphicObject):
    def __init__(self, w=None, h=None):
        self.draw = self.Draw(self)
        if not w is None and not h is None:
            self.w = w + 1
            self.h = h + 1
            self.reset()

    def reset(self):
        self.objects = GraphicObjectArray()
        self.graph = Graph(w=self.w, h=self.h)

    # draw methods (A-Z)

    def _draw_in_graph(self):
        self.graph.add_objects(self.objects)

    # aux methods (A-Z)

    def add_object(self, obj):
        self.objects.add(obj)

    def show(self, axes=False, frame=False):
        self.graph = Graph(w=self.w, h=self.h)
        self._draw_in_graph()
        self.graph.print(axes=axes, frame=frame)

    class Draw:
        def __init__(self, outer):
            self._canvas = outer

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
