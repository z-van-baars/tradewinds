

class Entity(object):
    def __init__(self, active_map, x, y):
        self.active_map = active_map
        self.x = x
        self.y = y

    def get_vitals(self):
        vitals = {}
        for attr_name in ("x",
                          "y"):
            vitals[attr_name] = getattr(self, attr_name)
        return vitals
