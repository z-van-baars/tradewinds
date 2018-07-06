import utilities as util
import pygame
import art
import ships


class Player(object):
    def __init__(self, x, y):
        self.column = x
        self.row = y
        starter_cog = ships.Cog()
        self.ship = starter_cog
        self.silver = 0
