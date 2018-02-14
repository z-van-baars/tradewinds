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
        self.stats = Stats()
        self.time = 0
        self.timer = 0

        self.active_map = None
        self.remove = False
        self.activation_mode = False
        self.build_menu = False
        self.build_candidate = "None"
        self.selected_construct = None
        self.reset_surfaces()

    def reset_surfaces(self):
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])


class Stats(object):
    def __init__(self):
        self.total_steps = 0
        self.resources = {"Wood": [],
                          "Food": [],
                          "Stone": [],
                          "Copper": [],
                          "Labor": []}
