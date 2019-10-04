import entity
from enum import Enum
import nav
import utilities as util


class AgentState(Enum):
    idle = 0
    move = 1


class Agent(entity.Entity):
    def __init__(self, active_map, x, y):
        super().__init__(active_map, x, y)
        self.tick_cycles = {AgentState.idle: self.idle_tick,
                            AgentState.move: self.move_tick}
        self.state = AgentState.idle
        self.ship = None
        """path object.  Should be None if there is no target"""
        self.path = None
        self.path_pts = None
        """Target Tile ID
        (for now this will always be chained to the target port / port ID)"""
        self.target_tile = None
        self.move_timer = 0
        self.move_timer_max = 0

    def get_vitals(self):
        vitals = {}
        for attr_name in ("x",
                          "y"):
            vitals[attr_name] = getattr(self, attr_name)
            vitals["ship"] = self.ship.get_vitals()
            vitals["target tile"] = self.target_tile

        return vitals

    def tick(self):
        self.tick_cycles[self.state]()

    def idle_tick(self):
        if self.target_tile is not None:
            self.state = AgentState.Move

    def move_tick(self):
        """we should not be here if both of these are None"""
        assert not (self.path is None and self.target_tile is None)
        self.check_path()
        if self.path is not None and self.check_move_timer():
            step = self.path.get_step()
            self.move(step.column, step.row)
        elif self.path is not None and not self.check_move_timer():
            self.move_timer -= 1
        elif self.path is None and self.target_tile is not None:
            self.set_path(self.get_path_to_target())
        """^^ From time to time the path object will get wiped, ^^
        usually for objects blocking the path.  In this case,
        we just want to re-path.  At the moment his does use up
        a full tick cycle, but it doesn't use the move_timer"""

    def check_path(self):
        """are there any more tiles left in the path?
        If not we should be at the target"""
        if len(self.path.steps) < 1:
            self.path = None
            self.clear_target()
            self.state = AgentState.idle
            return
        """This doesn't trigger yet since Constructs don't exist yet"""
        for each_step in self.path.steps:
            if each_step.is_occupied():  # is there a construct object in said tile?
                self.path = None

    def move(self, x, y):
        self.column = x
        self.row = y
        self.tile = self.active_map.game_tile_rows[y][x]
        self.ship.column = x
        self.ship.row = y
        self.ship.tile = self.tile
        self.move_timer = self.move_timer_max

    def get_path_to_target(self):
        new_path = nav.get_path(
            (self.column, self.row),
            self.active_map,
            (self.target_tile.column,
             self.target_tile.row))
        return new_path

    def set_path(self, new_path):
        self.path = new_path
        line_pts = []
        for step in self.path.steps:
            map_x = step.column
            map_y = step.row
            pixel_xy = util.get_screen_coords(map_x, map_y)
            line_pts.append(pixel_xy)
        self.move_timer_max = round((5.0 / self.ship.speed) * 10)
        self.state = AgentState.move

    def check_move_timer(self):
        if self.move_timer <= 0:
            return True
        return False

    def clear_target(self):
        self.target_tile = None
        self.path = None

