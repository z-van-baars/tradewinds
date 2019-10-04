

class GameTile(object):
    def __init__(self, column, row, biome):
        self.row = row  # X
        self.column = column  # Y
        self.biome = biome  # string
        self.terrain = None  # string
        self.resource = None  # string
        self.output = {}  # dict[string] = int
        self.water_flux = (0, 0, 0)  # threeple = (int, int, int)
        self.water_source = ([], 0)  # tuple = (list[int], int)
        self.bordered_edges = {}  # dict[tuple(int, int)] = bool

        self.construct = None  # None
        self.city = None  # City()
        self.owner = None  # City()
        self.nation = None  # Nation()

    def __lt__(self, other):
        return False

    def is_occupied(self):
        return self.construct

    def is_land(self):
        return self.biome not in ('lake',
                                  'shallows',
                                  'sea',
                                  'ocean')

    def get_vitals(self):
        vitals = {}
        for attr_name in ("row",
                          "column",
                          "biome",
                          "terrain",
                          "resource",
                          "output",
                          "water_flux",
                          "water_source",
                          "bordered_edges"):
            vitals[attr_name] = getattr(self, attr_name)
        return vitals

    def load_existing(self, records):
        for attr_name in ("row",
                          "column",
                          "biome",
                          "terrain",
                          "resource",
                          "output",
                          "water_flux",
                          "water_source",
                          "bordered_edges"):
            self.attr_name = records[attr_name]
