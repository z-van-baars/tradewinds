import pygame
import utilities
from game_map import Map
from mapgen import load_existing
from player import Player
import ui


class GameState(object):
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = pygame.time.Clock()
        self.console_log = []
        self.calendar = utilities.Calendar()

        self.game_speed = 60
        self.time = 0
        self.paused = False
        self.timer = 0

        self.draw_routes = True
        self.infinite_speed = False
        self.draw_borders = False

        self.active_map = None
        self.active_menus = []
        self.reset_surfaces()

    def load_external_state(self, records):
        self.game_speed = records["game_speed"]
        self.time = records["time"]
        self.paused = records["paused"]
        self.timer = records["timer"]

        self.draw_routes = records["draw_routes"]
        self.infinite_speed = records["infinite_speed"]
        self.draw_borders = records["draw_borders"]

        if "calendar" not in records:
            records["calendar"] = (1, 0, 1520)
        self.calendar.day = records["calendar"][0]
        self.calendar.month = records["calendar"][1]
        self.calendar.year = records["calendar"][2]
        self.calendar.set_month_string()

        self.active_map = Map(
            records["map dimensions"],
            (self.screen_width, self.screen_height))
        load_existing(self, records)

        self.active_map.player = Player(self, self.active_map)
        self.active_map.player.load_external(records["player"])

        x1, y1 = utilities.get_screen_coords(
            self.active_map.player.ship.column,
            self.active_map.player.ship.row)
        self.active_map.x_shift = (
            -x1 - 40 - self.background_width / 2 +
            self.screen_width / 2)
        self.active_map.y_shift = (
            -y1 - 40 + self.screen_height / 2)

        self.clock = pygame.time.Clock()
        mini_map = ui.MiniMap(self)
        calendar_menu = ui.CalendarMenu(self)
        self.active_menus.append(mini_map)
        self.active_menus.append(calendar_menu)

    def serial_prep(self):
        records = self.active_map.serial_prep()

        for attr_name in ("game_speed",
                          "time",
                          "paused",
                          "timer",
                          "draw_routes",
                          "infinite_speed",
                          "draw_borders",
                          "calendar"):
            records[attr_name] = getattr(self, attr_name)

        return records

    def reset_surfaces(self):
        self.screen = pygame.display.set_mode(
            [self.screen_width, self.screen_height],
            pygame.RESIZABLE)

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
    def background_width(self):
        return self.active_map.tile_display_layer.image.get_width()

    @property
    def background_height(self):
        return self.active_map.tile_display_layer.image.get_height()

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
        return (self.background_left,
                self.background_top,
                self.background_right,
                self.background_bottom,
                self.background_x_middle)

