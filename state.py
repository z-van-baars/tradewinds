import pygame
import construct
import utilities


class GameState(object):
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = pygame.time.Clock()
        self.calendar = utilities.Calendar()
        self.game_speed = 60
        self.time = 0
        self.timer = 0

        self.active_map = None
        self.player = None
        self.reset_surfaces()

    def reset_surfaces(self):
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
