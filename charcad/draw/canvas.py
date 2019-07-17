# canvas module

import math
from copy import deepcopy

from charcad.draw.graphic_object import GraphicObjectArray
from charcad.draw.point import Point
from charcad.draw.route import Route

from charcad.draw.utils import force_list, chrs


class Canvas:
    def __init__(self, w=None, h=None):
        self.draw = Draw(self)
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

    # aux methods

    def add_object(self, obj):
        self.objects.add(obj)

    def show(self, axes=False, frame=False):
        self.draw_in_graph()
        self.graph.print(axes=axes, frame=frame)


class Draw:
    def __init__(self, canvas):
        self._canvas = canvas
    
    def point(self, p):
        self._canvas.add_object(p)

    def route(self, *p, marker='.', origin_marker=None):
        if origin_marker is None:
            origin_marker = marker
        p = list(p)
        for i, item in enumerate(p):
            if isinstance(item, (tuple, list)):
                p[i] = Point(*item)
            elif isinstance(item, Point):
                p[i] = item
        route = Route()
        route.create_route(*p, marker=marker, origin_marker=origin_marker)
        self._canvas.add_object(route)


class Graph:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.grid = list()
        self.reset()

    def __repr__(self):
        return ''.join([''.join(row)+'\n' for row in self.grid])

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

    def print(self, frame=False, axes=False):
        grph = deepcopy(self)
        if frame:
            grph = add_frame(grph)
        if axes:
            grph = add_axes(grph)
        print(grph)

    def reset(self):
        for _ in range(self.h):
            self.grid.append([' '] * self.w)


def add_axes(grph):
    hlen = len(grph.grid)
    wlen = len(grph.grid[0])

    # axis order of gratness
    yg = math.floor(math.log10(hlen)) + 1
    xg = math.floor(math.log10(wlen)) + 1

    # check offset (caused by frame)
    offset_h = int((hlen - grph.h) / 2)
    offset_w = int((wlen - grph.w) / 2)

    # y axis (with frame and axis compensation)
    yaxis = (
        [' ' * yg] * offset_h
        + [str(grph.h - y - 1).zfill(yg) for y in range(grph.h)]
        + [' ' * yg] * offset_h
    )

    # x axis (with frame and axis compensation)
    xaxis = list()
    for i in range(xg):
        n = 10**i
        xaxis.append(
            [' ' * (yg + offset_w)]
            + [str(int(x/n) % 10) if (x % n) ==
               0 else ' ' for x in range(grph.w)]
        )

    # add to original grid
    grph.grid = (
        [[z[0]] + z[1] for i, z in enumerate(zip(yaxis, grph.grid))]
        + xaxis
    )
    return grph


def add_frame(grph):
    grphlen = grph.w
    for i, item in enumerate(grph.grid):
        grph.grid[i] = [chrs.ud] + item + [chrs.ud]
    li = [[chrs.ur] + grphlen * [chrs.lr] + [chrs.rd]]
    lf = [[chrs.dr] + grphlen * [chrs.lr] + [chrs.ru]]
    grph.grid = li + grph.grid + lf
    return grph
