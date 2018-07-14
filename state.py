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
        self.active_menus = []
        self.reset_surfaces()

    def reset_surfaces(self):
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

    def clear_menutype(self, typematch):
        offending_menus = []
        for menu in self.active_menus:
            if any((type(menu) == subtype) for subtype in typematch):
                offending_menus.append(menu)
        for each_offender in offending_menus:
            self.active_menus.remove(each_offender)

    @property
    def background_left(self):
        return self.active_map.x_shift

    @property
    def background_top(self):
        return self.active_map.y_shift

    @property
    def background_x_middle(self):
        return 20 + (self.background_left + self.background_width / 2)

    @property
    def background_bottom(self):
        return (self.background_top + self.background_height)

    @property
    def background_right(self):
        return (self.background_left + self.background_width)

    @property
    def display_parameters(self):
        return (self.background_left, self.background_top, self.background_right, self.background_bottom, self.background_x_middle)
