import math


# properties

class DrawingChars:
    def __init__(self):
        self.ud = '│'
        self.ur = '┌'
        self.dr = '└'
        self.ru = '┘'
        self.rd = '┐'
        self.lr = '─'

        self.ilr = '_'
        self.oin = '┼'
        self.din = '╳'
        self.dru = '╱'
        self.drd = '╲'


chrs = DrawingChars()


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
    if isinstance(var, (int, float)):
        var = [var]
    elif not isinstance(var, list):
        var = list(var)
    return var


# text formatters

ESCAPE = ['\033[', '\033[0m']
STYLES = {
    'none': '0',
    'bold': '1',
    'negative': '2',
    'negative2': '5',
    'underline': '4',
}
COLORS = {
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'purple': '35',
    'cyan': '36',
    'white': '37',
    'none': '38'
}
BACKGROUND_COLORS = {
    'black': '40',
    'red': '41',
    'green': '42',
    'yellow': '43',
    'blue': '44',
    'purple': '45',
    'cyan': '46',
    'white': '47',
    'none': '48',
}


class Formatter:
    class _Styles:
        def __init__(self):
            self.__dict__ = STYLES

    class _Colors:
        def __init__(self):
            self.__dict__ = COLORS

    class _BackgroundColors:
        def __init__(self):
            self.__dict__ = BACKGROUND_COLORS

    def __init__(self):
        # formats
        self.styles = self._Styles()
        self.colors = self._Colors()
        self.background_colors = self._BackgroundColors()
        # config
        self.style = self.styles.none
        self.color = self.colors.none
        self.background_color = self.background_colors.none
    
    def __repr__(self):
        return self.format('Hello! I am Formatter ' + str(id(self)))

    def set_background_color(self, background_color):
        self.background_color = self.background_colors\
            .__dict__[background_color.lower()]

    def set_color(self, color):
        self.color = self.colors.__dict__[color.lower()]

    def set_style(self, style):
        self.style = self.styles.__dict__[style.lower()]

    def format(self, text):
        style = self.style
        color = self.color
        bgcolor = self.background_color + 'm'
        fmt = [style, color, bgcolor]
        if all(fmt):
            text_out = (';'.join(fmt) + text).join(ESCAPE)
        else:
            text_out = text
        return text_out


# decorators
