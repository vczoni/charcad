
from charcad.draw.point import Point
from charcad.draw.vector import Vector
from charcad.draw.utils import calc_angle, calc_distance


class Route:

    def __init__(self):
        self.objects = dict()
    
    def add_object(self, obj, name):
        self.objects.update({name: obj})
    
    def add_point(self, p):
        self.add_object(p, 'point_'+str(len(self.objects)))

    def create_route(self, *points, marker='.', seek_angle=False, factors=(1, 1)):
        for point, next_point in zip(points[0:-1], points[1:]):
            point.marker = marker
            self.connect(point, next_point, seek_angle, factors)

    def connect(self, p1, p2, seek_angle=False, factors=(1, 1)):
        current_point = p1
        target_point = p2
        target_angle = calc_angle(Vector(current_point), Vector(target_point))
        arrived = current_point == target_point
        while not arrived:
            next_points = [current_point + m for m in movements]
            distances = [calc_distance(p, target_point, factors)
                         for p in next_points]
            if seek_angle:
                next_angles = [calc_angle(Vector(p), Vector(target_point))-target_angle
                               for p in next_points]
                
            else:
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
