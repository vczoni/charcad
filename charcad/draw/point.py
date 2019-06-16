class Point:
    def __init__(self, x, y, marker='.'):
        self.x = x
        self.y = y
        self.marker = marker

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Point(self.x*other, self.y*other)
        else:
            raise Exception("'other' must be scalar.")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Point(self.x/other, self.y/other)
        else:
            raise Exception("'other' must be scalar.")

    def __eq__(self, other):
        return (self.x == other.x) & (self.y == other.y)

    def __getitem__(self, item):
        return [self.x, self.y][item]

    def __repr__(self):
        return 'point({}, {})'.format(self.x, self.y)

    def __floor__(self):
        return Point(int(self.x), int(self.y))

    def __round__(self, n=0):
        return Point(round(self.x, n), round(self.y, n))
