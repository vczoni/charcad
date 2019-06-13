class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        return (self.x == other.x) & (self.y == other.y)

    def __getitem__(self, item):
        return [self.x, self.y][item]

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)
