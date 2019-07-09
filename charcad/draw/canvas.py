# canvas module

import math
from copy import deepcopy

from charcad.draw.graphic_object import GraphicObjectArray
from charcad.draw.point import Point
from charcad.draw.route import Route

from charcad.draw.utils import force_list, chrs


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

    def drawroute(self, *p, marker='.', origin_marker='x'):
        p = list(p)
        for i, item in enumerate(p):
            if isinstance(item, (tuple, list)):
                p[i] = Point(*item)
            elif isinstance(item, Point):
                p[i] = item
        route = Route()
        route.create_route(*p, marker=marker, origin_marker=origin_marker)
        self.add_object(route)

    # aux methods

    def add_object(self, obj):
        self.objects.add(obj)

    def add_point(self, p):
        self.add_object(p)

    # inspecting functions (A-Z)

    def show(self, axes=False, frame=False):
        self.draw_in_graph()
        self.graph.print(frame=frame)


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

    def print(self, frame=False):
        grph = deepcopy(self)
        if frame:
            grphlen = len(grph.grid[0])
            for i, item in enumerate(grph.grid):
                grph.grid[i] = [chrs.ud] + item + [chrs.ud]
            li = [[chrs.ur] + grphlen * [chrs.lr] + [chrs.rd]]
            lf = [[chrs.dr] + grphlen * [chrs.lr] + [chrs.ru]]
            grph.grid = li + grph.grid + lf
        print(grph)

    def reset(self):
        for _ in range(self.h):
            self.grid.append([' '] * self.w)
