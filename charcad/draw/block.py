from charcad.draw.coordinates import Coordinates
from charcad.draw.canvas import Canvas
from charcad.draw.graph import add_frame


class Block(Canvas):
    def __init__(self, w, h, x=0, y=0, framed=True):
        super(Block, self).__init__(w=w, h=h)
        self.framed = framed
        if framed:
            self._add_frame()
        self.coord = Coordinates(x, y)
    
    def _add_frame(self):
        self.graph = add_frame(self.graph)
    
    def show(self, axes=False):
        self.reset_graph()
        if self.framed:
            self._add_frame()
        self.graph.add_objects(self.objects)
        self.graph.print(axes=axes, frame=False)
