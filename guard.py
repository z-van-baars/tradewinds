import agent
import ships
from enum import Enum


class GuardState(Enum):
    idle = 0
    aggro = 1
    home = 2
    patrol = 3


class Guard(agent.Agent):
    def __init__(self, active_map, x, y):
        super().__init__(active_map, x, y)
        self.ship = ships.Corvette(active_map, x, y)
        self.home_city = None
        self.tick_cycles = {GuardState.idle: self.idle_tick(),
                            GuardState.aggro: self.aggro_tick(),
                            GuardState.home: self.home_tick(),
                            GuardState.patrol: self.patrol_tick()}

    def idle_tick(self):
        pass

