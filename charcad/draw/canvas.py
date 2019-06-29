# canvas module

import math

from charcad.draw.gpharray import GraphicObjectArray
from charcad.draw.point import Point
from charcad.draw.route import Route

from charcad.draw.utils import force_list


class Canvas:
    def __init__(self, w=None, h=None):
        if not w is None and not h is None:
            self.new(w, h)

    # initializers (logical order)

    def new(self, w, h):
        self.w = w
        self._w = w + 1
        self.h = h
        self._h = h + 1
        self.reset()

    def reset(self):
        self.objects = GraphicObjectArray()
        self.grid = list()
        for _ in range(self._h):
            self.grid.append(list(range(self._w)))

    # draw methods (A-Z)

    def drawroute(self, *p, marker='.', origins=True, origin_marker='x',
                  seek_angle=False):
        p = list(p)
        for i, item in enumerate(p):
            if isinstance(item, (tuple, list)):
                p[i] = Point(*item)
        route = Route()
        route.create_route(*p, marker=marker)
        if origins:
            vals = [*route.objects.values()]
            keys = [*route.objects]
            vals[0].marker = origin_marker
            vals[-1].marker = origin_marker
            route.objects.update(dict(zip(keys, vals)))
        self.add_object(route, 'route_'+str(len(self.objects)))

    def drawpoint(self, *p, marker='.'):
        if isinstance(p[0], int):
            self.add_point(Point(*p, marker=marker))
        elif isinstance(p[0], (list, tuple)):
            for item in p:
                self.drawpoint(*item, marker=marker)
        elif isinstance(p[0], Point):
            for item in p:
                self.drawpoint(*item, item.marker)

    def frame(self, graph):
        ud = chrs.ud
        ur = chrs.ur
        dr = chrs.dr
        ru = chrs.ru
        rd = chrs.rd
        rl = chrs.lr
        midspace = (self._w - 2)
        for i in range(len(graph)):
            y = flip_lst_y(graph, i)
            if y == 0:
                graph[i] = dr + midspace*rl + ru
            elif y < len(graph) - 1:
                graph[i] = ud + midspace*' ' + ud
            elif y == len(graph) - 1:
                graph[i] = ur + midspace*rl + rd
        return graph

    # aux methods

    def add_object(self, obj, name):
        self.objects.update({name: obj})

    def add_point(self, p):
        self.add_object(p, 'point_'+str(len(self.objects)))

    def _object_printer(self, objects, graph):
        for _, obj in objects.items():
            if isinstance(obj, Point):
                graph = self._point_printer(graph, obj)
            elif isinstance(obj, Route):
                graph = self._object_printer(obj.objects, graph)
        return graph

    def _point_printer(self, graph, point):
        x = point.x
        y = flip_lst_y(graph, point.y)
        graph[y] = graph[y][0:x] + point.marker + graph[y][x+1:]
        return graph

    # inspecting functions (A-Z)

    def show(self, axes=False, frame=True):
        # init graph
        graph = mkgraph(self._w, self._h)

        # add frame (if requested)
        if frame:
            graph = self.frame(graph)

        # add axes (if requested)
        axes = force_list(axes)
        if len(axes) == 1:
            axes += axes
        # x axis
        if axes[0]:
            x_order = math.floor(math.log10(self._w))
            y_order = math.floor(math.log10(self._h))
            rr = list()
            for n in range(x_order+1):
                rri = ' ' * (y_order+1)
                o = 10**n
                for i in range(self._w):
                    if i % o == 0:
                        s = str(int(i/o) % 10)
                    else:
                        s = ' '
                    rri += s
                rr.append(rri)
        else:
            rr = ''
        # y axis
        if axes[1]:
            y_order = math.floor(math.log10(self._h))
            def c1(yi): return str(flip_lst_y(graph, yi)).zfill(y_order+1)
        else:
            def c1(yi): return ''

        # draw objects in graph
        graph = self._object_printer(self.objects, graph)

        # print objects and axes
        for i, r in enumerate(graph):
            print(c1(i) + r)
        for r in rr:
            print(r)


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


def mkgraph(w, h):
    graph = list()
    for _ in range(h):
        graph.append(' ' * w)
    return graph


def flip_lst_y(lst, yi):
    return len(lst) - yi - 1
