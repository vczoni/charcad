# canvas module

import math

from charcad.draw.graphic_object import GraphicObjectArray
from charcad.draw.point import Point
from charcad.draw.route import Route

from charcad.draw.utils import force_list


class Canvas:
    def __init__(self, w=None, h=None):
        if not w is None and not h is None:
            self.new(w, h)

    # initializers (logical order)

    def new(self, w, h):
        self.w = w + 1
        self.h = h + 1
        self.reset()

    def reset(self):
        self.objects = GraphicObjectArray()
        self.graph = Graph(self.w, self.h)

    # draw methods (A-Z)

    def draw_in_graph(self):
        self.graph.add_objects(self.objects)

    def drawroute(self, *p, marker='.', origins=True, origin_marker='x',
                  seek_angle=False):
        p = list(p)
        for i, item in enumerate(p):
            if isinstance(item, (tuple, list)):
                p[i] = Point(*item)
        route = Route()
        route.create_route(*p, marker=marker)
        if origins:
            vals = route.objects.values
            keys = route.objects.keys
            vals[0].marker = origin_marker
            vals[-1].marker = origin_marker
            route.objects.update(dict(zip(keys, vals)))
        self.add_object(route)

    def drawpoint(self, *p, marker='.'):
        if isinstance(p[0], int):
            self.graph.add_point(Point(*p, marker=marker))
        elif isinstance(p[0], (list, tuple)):
            for item in p:
                self.drawpoint(*item, marker=marker)
        elif isinstance(p[0], Point):
            for item in p:
                self.drawpoint(*item, item.marker)

    # aux methods

    def add_object(self, obj):
        self.objects.add(obj)

    def add_point(self, p):
        self.add_object(p)

    # inspecting functions (A-Z)

    def show(self, axes=False, frame=True):
        self.draw_in_graph()
        self.graph.print()


class Graph:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.grid = list()
        self.reset()

    def __repr__(self):
        printstr = str()
        for row in self.grid:
            for item in row:
                printstr += item
            printstr += '\n'
        return printstr

    def add_objects(self, graphicArray):
        for obj in graphicArray:
            if isinstance(obj, GraphicObjectArray):
                self.add_objects(obj)
            elif isinstance(obj, Point):
                self.add_point(obj)
            else:
                self.add_objects(obj.objects)

    def add_point(self, point):
        x = point.x
        y = self.flipud(point.y)
        self.grid[y][x] = point.marker

    def flipud(self, yi):
        return len(self.grid) - yi - 1

    def inspect(self):
        [print(item) for item in [row for row in self.grid]]

    def print(self):
        print(self.__repr__())

    def reset(self):
        for _ in range(self.h):
            self.grid.append([' '] * self.w)


class DrawingChars:
    def __init__(self):
        self.ud = '│'
        self.ur = '┌'
        self.dr = '└'
        self.ru = '┘'
        self.rd = '┐'
        self.lr = '─'
        self.i = '┼'

        self.dru = '╱'
        self.drd = '╲'
        self.dlr = '_'
        self.di = '╳'


chrs = DrawingChars()
