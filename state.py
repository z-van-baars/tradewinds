import pygame
import utilities


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
        self.ships = set()
        self.player = None
        self.active_menus = []
        self.reset_surfaces()

    def load_external_state(self, ext_state):
        self.game_speed = ext_state.game_speed
        self.time = ext_state.time
        self.paused = ext_state.paused
        self.timer = ext_state.timer

        self.draw_routes = ext_state.draw_routes
        self.infinite_speed = ext_state.infinite_speed
        self.draw_borders = ext_state.draw_borders

        self.active_map = ext_state.active_map
        self.ships = ext_state.ships
        self.player = ext_state.player

        self.unpack_string_buffers()

    def pack_string_buffers(self):
        self.active_map.tile_display_layer = None
        self.active_map.terrain_display_layer = None
        self.active_map.resource_display_layer = None
        self.active_map.building_display_layer = None
        self.active_map.nation_border_display_layer = None
        self.screen = None

        for each_ship in self.active_map.ships:
            pygame.image.tostring(each_ship.image)

    def unpack_string_buffers(self):
        for each_ship in self.active_map.ships:
            pygame.image.fromstring(each_ship.image)
        self.active_map.prepare_surfaces()
        self.reset_surfaces()

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

