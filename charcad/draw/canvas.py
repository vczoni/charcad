# canvas module

from charcad.draw.utils import force_list
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
        elif isinstance(possible_integer, list) or isinstance(possible_integer, tuple):
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


def flip_lst_y(lst, yi):
    return len(lst) - yi - 1


def route_assist(x1, x2, y1, y2):
    if x1 > x2:
        aux = x1
        x1 = x2
        x2 = aux
        aux = y1
        y1 = y2
        y2 = aux
    directions = [math.pi/2, math.pi/4, 0, -math.pi/4, -math.pi/2]
    movements = [
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
    ]
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    n = max(dx, dy)
    cx = x1
    cy = y1
    route = list()
    for _ in range(n):
        dx = x2 - cx
        dy = y2 - cy
        if dx > 0:
            a = math.atan(dy / dx)
        elif dx == 0:
            a = math.atan(dy * math.inf)
        else:
            raise Exception("cx is bigger than x2!")
        diff = [abs(x-a) for x in directions]
        idx = diff.index(min(diff))
        cx += movements[idx][0]
        cy += movements[idx][1]
        route.append((cx, cy))
    return route
