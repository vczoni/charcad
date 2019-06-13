# canvas module

from charcad.draw.utils import force_list
from charcad.draw.point import Point
import math


class Canvas:
    def __init__(self):
        self.chrs = DrawingChars()

    # initializers (logical order)

    def new(self, w, h, frame=True):
        self.w = w
        self._w = w + 1
        self.h = h
        self._h = h + 1
        self.graph = list()
        self.grid = list()
        self.reset_graph()
        if frame:
            self.frame()

    def reset_graph(self):
        for _ in range(self.h + 1):
            self.graph.append(' ' * (self._w))
            self.grid.append(list(range(self._w)))

    def frame(self):
        ud = self.chrs.ud
        ur = self.chrs.ur
        dr = self.chrs.dr
        ru = self.chrs.ru
        rd = self.chrs.rd
        rl = self.chrs.lr
        midspace = (self._w - 2)
        for i in range(len(self.graph)):
            y = flip_lst_y(self.graph, i)
            if y == 0:
                self.graph[i] = dr + midspace*rl + ru
            elif y < len(self.graph) - 1:
                self.graph[i] = ud + midspace*' ' + ud
            elif y == len(self.graph) - 1:
                self.graph[i] = ur + midspace*rl + rd

    # draw functions (A-Z)

    def drawroute(self, x1, y1, x2, y2, marker='.', origins=True, origin_marker='x'):
        route = route_assist(x1, x2, y1, y2)
        print(route)
        self.drawpoint(route, marker=marker)
        if origins:
            self.drawpoint([(x1, y1), (x2, y2)], marker=origin_marker)

    def drawpoint(self, *p, **kw):
        args = {
            'marker': '.'
        }
        args.update(kw)
        marker = args['marker']
        possible_integer = p[0]
        if isinstance(possible_integer, int):
            self._point_assist(*p, marker=marker)
        elif (isinstance(possible_integer, list)
              or isinstance(possible_integer, Point)
              or isinstance(possible_integer, tuple)):
            for item in p:
                self.drawpoint(*item, **kw)

    def _point_assist(self, x=0, yi=0, marker='.'):
        y = flip_lst_y(self.graph, yi)
        ri = self.graph[y]
        r = ri[0:x] + marker + ri[x+1:]
        self.graph[y] = r

    # inspecting functions (A-Z)

    def show(self, axis=False):
        if axis:
            x_order = math.floor(math.log10(self._w))
            y_order = math.floor(math.log10(self._h))
            def c1(yi): return str(flip_lst_y(self.graph, yi)).zfill(y_order+1)
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
            def c1(yi): return ''
            rr = ''
        for i, r in enumerate(self.graph):
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


def calc_distance(p1, p2, factors=(1, 1)):
    dx = (p2[0] - p1[0]) * factors[0]
    dy = (p2[1] - p1[1]) * factors[1]
    return math.hypot(dx, dy)


def flip_lst_y(lst, yi):
    return len(lst) - yi - 1


def route_assist(x1, x2, y1, y2, factors=(25/60, 1)):
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
    route = list()
    target_point = Point(x2, y2)
    cx = x1
    cy = y1
    arrived = cx == x2 & cy == y2
    while not arrived:
        current_point = Point(cx, cy)
        next_points = [current_point + m for m in movements]
        distances = [calc_distance(p, target_point, factors)
                     for p in next_points]
        print('movements')
        print(movements)
        print('current_point')
        print(current_point)
        print('target_point')
        print((x2, y2))
        print('distances')
        print(distances)
        print('  ')
        idx = distances.index(min(distances))
        cx += movements[idx][0]
        cy += movements[idx][1]
        route.append(Point(cx, cy))
        arrived = (cx == x2) & (cy == y2)
    return route
