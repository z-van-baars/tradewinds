import utilities as util
import pygame
import art
import ships


class Player(object):
    def __init__(self, active_map):
        self.active_map = active_map
        starter_cog = ships.Cog(active_map, 0, 5)
        self.ship = starter_cog
        self.silver = 0
