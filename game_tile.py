

class GameTile(object):
    def __init__(self, column, row, biome):
        self.row = row
        self.column = column
        self.construct = None
        self.biome = biome
        self.terrain = None

    def __lt__(self, other):
        return False

    def is_occupied(self):
        if not self.construct:
            return False
        return True
