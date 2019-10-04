

class Entity(object):
    def __init__(self, active_map, column, row):
        self.active_map = active_map
        self.row = column
        self.row = row

    def get_vitals(self):
        vitals = {}
        for attr_name in ("column",
                          "row"):
            vitals[attr_name] = getattr(self, attr_name)
        return vitals
