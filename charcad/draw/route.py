# route

from charcad.draw.graphic_object import GraphicObject, GraphicObjectArray
from charcad.draw.point import Point
from charcad.draw.vector import Vector
from charcad.draw.utils import calc_angle, calc_distance


class Route(GraphicObject):

    def __init__(self):
        self.objects = GraphicObjectArray()

    def __repr__(self):
        return 'Route at <%s>' % id(self)

    def add_object(self, obj):
        self.objects.add(obj)

    def add_point(self, p):
        self.add_object(p)

    def create_route(self, *points, marker='.', factors=(1, 1)):
        for point, next_point in zip(points[0:-1], points[1:]):
            point.marker = marker
            self.connect(point, next_point, factors)

    def connect(self, p1, p2, factors=(1, 1)):
        current_point = p1
        target_point = p2
        arrived = current_point == target_point
        self.add_point(current_point)
        while not arrived:
            next_points = [current_point + m for m in movements]
            distances = [calc_distance(p, target_point, factors)
                         for p in next_points]
            idx = distances.index(min(distances))
            current_point += movements[idx]
            self.add_point(current_point)
            arrived = current_point == target_point


movements = [
    Point(0, 1),
    Point(1, 1),
    Point(1, 0),
    Point(1, -1),
    Point(0, -1),
    Point(-1, -1),
    Point(-1, 0),
    Point(-1, 1),
]
