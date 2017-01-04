


class MapNode(object):
    def __init__(self, x, y, passable):
        self.x = x
        self.y = y
        self.neighbors = []
        self.passable = passable
        self.cost = 1


class MapEdge(object):
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.points = []
        self.cost = 1