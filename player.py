import ships
import agent
import enum


class PlayerState(enum.Enum):
    idle = 0
    move = 1


class Player(agent.Agent):
    def __init__(self, game_state, active_map):
        super().__init__(active_map, 0, 0)
        self.game_state = game_state
        self.active_map = active_map
        starter_cog = ships.Cog(active_map, 0, 5)
        self.ship = starter_cog
        self.silver = 0

    def get_vitals(self):
        vitals = {}
        for attr_name in ("x",
                          "y",
                          "silver"):
            vitals[attr_name] = getattr(self, attr_name)
        vitals["ship"] = self.ship.get_vitals()
        vitals["target tile"] = self.target_tile

        return vitals

    def load_existing(self, records):
        for attr_name in ("x",
                          "y",
                          "silver"):
            self.attr_name = records[attr_name]
        ShipClass = ships.ship_types[records["ship"]["hull_class"]]
        new_ship = ShipClass(self.active_map, records["ship"]["x"], records["ship"]["y"])
        new_ship.load_existing(records["ship"])
        self.ship = new_ship
        self.target_tile = records["target tile"]

    def move_tick(self):
        if self.path and self.check_move_timer():
            step = self.path.get_step()
            self.move(step.column, step.row)
            self.check_path()
        elif self.path and not self.check_move_timer():
            self.move_timer -= 1
            if self.game_state.infinite_speed:
                self.move_timer = 0
