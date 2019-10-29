import math
import numpy as np
from copy import deepcopy

from charcad.draw.coordinates import Coordinates
from charcad.draw.utils import force_list, chrs


_empty_grid = np.array([[' ']])


class GraphicObject:
    def __init__(self, x=0, y=0):
        if isinstance(x, Coordinates):
            coord = x
        else:
            coord = Coordinates(x, y)
        self.coord = coord
        self.graph = None

    @property
    def x(self):
        return self.coord.x

    @property
    def y(self):
        return self.coord.y


class GraphicObjectArray:
    def __init__(self):
        self._objects = dict()

    def __getitem__(self, key):
        if not isinstance(key, str):
            k = self.keys
            k.sort()
            key = k[key]
        return self._objects[key]

    def __len__(self):
        return len(self._objects)

    def __repr__(self):
        z = zip(self.keys, self.values)
        return 'Graphic Object Array[\n    %s\n]' % \
            ',\n    '.join([(k + ': %s') % v for k, v in z])

    @property
    def keys(self):
        return list(self._objects)

    @property
    def values(self):
        return list(self._objects.values())

    def add(self, obj):
        name = 'object_{:04d}'.format(self.__len__())
        self._objects.update({name: obj})

    def remove(self, key):
        del self._objects[key]

    def update(self, item):
        self._objects.update(item)


class Graph:
    def __init__(self, grid=None, w=0, h=0):
        if grid is None:
            grid = np.full((h, w), ' ', dtype=object)
        elif isinstance(grid, str):
            grid = np.array([[grid]])
        elif isinstance(grid, np.ndarray):
            pass
        else:
            raise TypeError('grid cant be numeric.')
        self.grid = grid

    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.grid])

    def __len__(self):
        return len(self.grid)

    def __getitem__(self, key):
        return Graph(self.grid[key])

    def __setitem__(self, key, value):
        # i utterly hate this
        key = list(key)
        for i, k in enumerate(key):
            if not isinstance(k, slice):
                key[i] = slice(k, k+1)
        key = tuple(key)
        self.grid[key] = value.grid

    @property
    def h(self):
        return self.grid.shape[0]

    @property
    def w(self):
        return self.grid.shape[1]

    @property
    def shape(self):
        return (self.h, self.w)

    def add_objects(self, graphicArray, transparency=True):
        for obj in graphicArray:
            if isinstance(obj, GraphicObjectArray):
                self.add_objects(obj)
            elif isinstance(obj, GraphicObject):
                self.add_graph(obj)
            else:
                raise TypeError(
                    "obj must be GraphicObject or GraphicObjectArray.")

    def add_graph(self, obj, x=0, y=0, transparency=True):
        if isinstance(x, Coordinates):
            coord_other = x
        else:
            coord_other = Coordinates(x, y)
        coord = obj.coord + coord_other
        xi = coord.x
        xf = coord.x + obj.graph.w
        yf = self.flipud(coord.y - 1)
        yi = self.flipud(coord.y - 1 + obj.graph.h)
        x_slice = slice(xi, xf)
        y_slice = slice(yi, yf)
        if transparency:
            new_subgraph = self[y_slice, x_slice].no_background_draw(obj.graph)
        else:
            new_subgraph = obj.graph
        self[y_slice, x_slice] = new_subgraph

    def copy(self):
        return Graph(self.grid.copy())

    def flipud(self, yi):
        return self.h - yi - 1

    def inspect(self):
        [print(item) for item in [row for row in self.grid]]

    def isempty(self):
        return self.grid == _empty_grid

    def no_background_draw(self, other, rng=None):
        gph_out = self.copy()
        for i in range(self.h):
            for j in range(self.w):
                iother = other[i, j]
                if not iother.isempty():
                    gph_out[i, j] = iother[0, 0]
        return gph_out

    def print(self, frame=False, axes=False):
        grph = deepcopy(self)
        if frame:
            grph = add_frame(grph)
        if axes:
            grph = add_axes(grph, self.w, self.h)
        print(grph)


def add_axes(grph, w, h):
    # axis order of gratness
    yg = math.floor(math.log10(grph.h)) + 1
    xg = math.floor(math.log10(grph.w)) + 1
    # check offset (caused by frame)
    offset_h = int((grph.h - h) / 2)
    offset_w = int((grph.w - w) / 2)
    # y axis (with frame and axis compensation)
    yaxis = (
        [' ' * yg] * offset_h
        + [str(h - y - 1).zfill(yg) for y in range(h)]
        + [' ' * yg] * offset_h
    )
    # x axis (with frame and axis compensation)
    xaxis = list()
    for i in range(xg):
        n = 10**i
        xaxis.append(
            [' ' * yg]
            + [' '] * offset_w
            + [str(int(x/n) % 10) if (x % n) == 0
               else ' ' for x in range(w)]
            + [' '] * offset_w
        )
    # add to original grid
    grph.grid = np.c_[yaxis, grph.grid]
    grph.grid = np.r_[grph.grid, xaxis]
    return grph


def add_frame(grph):
    li = [[chrs.ur] + grph.w * [chrs.lr] + [chrs.rd]]
    lf = [[chrs.dr] + grph.w * [chrs.lr] + [chrs.ru]]
    grph.grid = np.c_[[chrs.ud] * grph.h, grph.grid, [chrs.ud] * grph.h]
    grph.grid = np.r_[li, grph.grid, lf]
    return grph
