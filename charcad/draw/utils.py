import math


# properties


# fuctions

def calc_angle(v1, v2):
    return math.acos(clamp(v1.dot(v2)/abs(v1)*abs(v2), 0, 1))


def calc_distance(p1, p2, factors=(1, 1)):
    dx = (p2[0] - p1[0]) * factors[0]
    dy = (p2[1] - p1[1]) * factors[1]
    return math.hypot(dx, dy)


def clamp(val, minval, maxval):
    return max(min(val, maxval), minval)


def force_list(var):
    if not isinstance(var, list):
        var = [var]
    return var


def isnumeric(var):
    return isinstance(var, (float, int))
