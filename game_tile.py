

class GameTile(object):
    def __init__(self, column, row, biome):
        self.row = row  # X
        self.column = column  # Y
        self.construct = None
        self.biome = biome
        self.terrain = None
        self.resource = None
        self.water_flux = 0
        self.water_in = 0
        self.water_out = 0

    def __lt__(self, other):
        return False

    def is_occupied(self):
        if not self.construct:
            return False
        return True