import utilities
import pygame
import art


class Player(object):
    def __init__(self, x, y):
        self.column = x
        self.row = y
        self.image = pygame.Surface([30, 30])
        self.image.blit(art.cog_icon, [0, 0])
