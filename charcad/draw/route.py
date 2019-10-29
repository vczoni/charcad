# route

from charcad.draw.coordinates import Coordinates
from charcad.draw.graphic_object import GraphicObject, GraphicObjectArray, Graph
from charcad.draw.basic_geom import Point
from charcad.draw.vector import Vector
from charcad.draw.utils import calc_angle, calc_distance


class Route(GraphicObject):

    def __init__(self):
        super(Route, self).__init__()
        self.objects = GraphicObjectArray()

    def __repr__(self):
        return 'Route at <%s>' % id(self)

    @property
    def origin(self):
        x = min([obj.coord.x for obj in self.objects])
        y = min([obj.coord.y for obj in self.objects])
        self.coord = Coordinates(x, y)
        return self.coord

    @property
    def h(self):
        return (max([obj.coord.y for obj in self.objects])
                - min([obj.coord.y for obj in self.objects])
                + 1)

    @property
    def w(self):
        return (max([obj.coord.x for obj in self.objects])
                - min([obj.coord.x for obj in self.objects])
                + 1)

    def add_point(self, p, update=False):
        self.objects.add(p)
        if update:
            self.update_graph()

    def create_route(self, *points, marker='.', origin_marker='.'):
        for point, next_point in zip(points[0:-1], points[1:]):
            point.set_marker(marker)
            self.connect(point, next_point)
        self.objects[0].set_marker(origin_marker)
        self.objects[-1].set_marker(origin_marker)
        self.update_graph()

    def connect(self, p1, p2):
        current_point = p1
        target_point = p2
        arrived = current_point == target_point
        self.add_point(current_point)
        while not arrived:
            next_points = [current_point + m for m in movements]
            distances = [calc_distance(p, target_point)
                         for p in next_points]
            idx = distances.index(min(distances))
            current_point += movements[idx]
            self.add_point(current_point)
            arrived = current_point == target_point

    def update_graph(self):
        self.graph = Graph(w=self.w, h=self.h)
        origin = self.origin
        for obj in self.objects:
            obj.coord -= origin
            self.graph.add_graph(obj)


movements = [
    Coordinates(0, 1),
    Coordinates(1, 1),
    Coordinates(1, 0),
    Coordinates(1, -1),
    Coordinates(0, -1),
    Coordinates(-1, -1),
    Coordinates(-1, 0),
    Coordinates(-1, 1),
]
