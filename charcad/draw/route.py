
import math

from charcad.draw.point import Point
from charcad.draw.vector import Vector
from charcad.draw.utils import calc_angle, calc_distance, force_list


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
        target_vector = Vector(target_point-current_point)
        arrived = current_point == target_point
        self.add_point(current_point)
        while not arrived:
            next_points = [current_point + m for m in movements]
            distances = [calc_distance(p, target_point, factors)
                         for p in next_points]
            if seek_angle:
                try:
                    angles = [calc_angle(Vector(target_point-p), target_vector)
                              for p in next_points]
                except:
                    angles = [calc_angle(Vector(target_point-current_point), target_vector)
                              for p in next_points]
                idx = normalize_and_compare(vectors=[distances, angles],
                                            limits=['self', (0, math.pi/8)], fun='min')
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


def normalize(vector, limits):
    for i, item in enumerate(vector):
        vector[i] = (vector[i] - limits[0])/(limits[1] - limits[0])
    return vector


def normalize_and_compare(vectors, limits, fun='min'):
    for i, limit in enumerate(limits):
        if isinstance(limit, str):
            if limit == 'self':
                limits[i] = (min(vectors[i]), max(vectors[i]))
            else:
                raise Exception(limit.join("''") + ' is not supported.')
    nvectors = list()
    for vector, limit in zip(vectors, limits):
        nvectors.append(normalize(vector, limit))
    sum_vector = [0 for _ in range(len(nvectors[0]))]
    for nvector in nvectors:
        sum_vector = [x+y for x, y in zip(nvector, sum_vector)]
    if fun == 'min':
        target = min(sum_vector)
    elif fun == 'max':
        target = max(sum_vector)
    else:
        raise Exception(fun.join("''") + ' is not supported.')
    return sum_vector.index(target)
