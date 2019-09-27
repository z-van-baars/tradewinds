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

    def move_tick(self):
        if self.path and self.check_move_timer():
            step = self.path.get_step()
            self.move(step.column, step.row)
            self.check_path()
        elif self.path and not self.check_move_timer():
            self.move_timer -= 1
            if self.game_state.infinite_speed:
                self.move_timer = 0
