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
        self.ship = None
        self.silver = 0

    def get_vitals(self):
        vitals = {}
        for attr_name in ("column",
                          "row",
                          "silver"):
            vitals[attr_name] = getattr(self, attr_name)
        vitals["ship"] = self.ship.get_vitals()
        vitals["target tile"] = self.target_tile

        return vitals

    def load_external(self, records):
        for attr_name in ("column",
                          "row",
                          "silver"):
            setattr(self, attr_name, records[attr_name])
        ShipClass = ships.ship_types[records["ship"]["hull_class"]]
        new_ship = ShipClass(
            self.active_map, records["ship"]["column"],
            records["ship"]["row"])
        new_ship.load_external(records["ship"])
        self.ship = new_ship
        self.target_tile = records["target tile"]

    def move_tick(self):
        """we should not be here if both of these are None"""
        assert not (self.path is None and self.target_tile is None)
        if self.path is not None and self.check_move_timer():
            step = self.path.get_step()
            self.move(step.column, step.row)
        elif self.path is not None and not self.check_move_timer():
            self.move_timer -= 1
            if self.game_state.infinite_speed:
                self.move_timer = 0
        elif self.path is None and self.target_tile is not None:
            self.set_path(self.get_path_to_target())
        self.check_path()
        """^^ From time to time the path object will get wiped, ^^
        usually for objects blocking the path.  In this case,
        we just want to re-path.  At the moment his does use up
        a full tick cycle, but it doesn't use the move_timer"""
