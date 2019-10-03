import utilities as util
import pygame
import art
import math
import random
import pickle


context_menu = pygame.image.load('art/menus/context_menu.png')
tile_info_pane = pygame.image.load('art/menus/tile_info_pane.png')
impassable_popup_pane = pygame.image.load('art/menus/impassable_popup_pane.png')
city_menu_pane = pygame.image.load('art/menus/city_menu_pane.png')
market_menu_pane = pygame.image.load('art/menus/market_screen.png')
quantity_popup = pygame.image.load('art/menus/quantity_popup.png')


# City Menu Buttons
leave_r_img = pygame.image.load('art/buttons/leave_regular.png')
leave_h_img = pygame.image.load('art/buttons/leave_hover.png')

market_r_img = pygame.image.load('art/buttons/market_regular.png')
market_h_img = pygame.image.load('art/buttons/market_hover.png')

tavern_r_img = pygame.image.load('art/buttons/tavern_regular.png')
tavern_h_img = pygame.image.load('art/buttons/tavern_hover.png')
shipyard_r_img = pygame.image.load('art/buttons/shipyard_regular.png')
shipyard_h_img = pygame.image.load('art/buttons/shipyard_hover.png')

# Context Menu Buttons

cancel_r_img = pygame.image.load('art/buttons/cancel_regular.png')
cancel_h_img = pygame.image.load('art/buttons/cancel_hover.png')

done_r_img = pygame.image.load('art/buttons/done_regular.png')
done_h_img = pygame.image.load('art/buttons/done_hover.png')

move_r_img = pygame.image.load('art/buttons/move_to_regular.png')
move_h_img = pygame.image.load('art/buttons/move_to_hover.png')

enter_city_r_img = pygame.image.load('art/buttons/enter_city_regular.png')
enter_city_h_img = pygame.image.load('art/buttons/enter_city_hover.png')

tile_info_r_img = pygame.image.load('art/buttons/tile_info_regular.png')
tile_info_h_img = pygame.image.load('art/buttons/tile_info_hover.png')

ok_r_img = pygame.image.load('art/buttons/ok_button_regular.png')
ok_h_img = pygame.image.load('art/buttons/ok_button_hover.png')

# Market Screen Buttons
x_button_r_img = pygame.image.load('art/buttons/x_regular.png')
x_button_h_img = pygame.image.load('art/buttons/x_hover.png')

arrow_u_r_img = pygame.image.load('art/buttons/arrow_up_regular.png')
arrow_u_h_img = pygame.image.load('art/buttons/arrow_up_hover.png')
arrow_d_r_img = pygame.image.load('art/buttons/arrow_down_regular.png')
arrow_d_h_img = pygame.image.load('art/buttons/arrow_down_hover.png')
arrow_r_r_img = pygame.image.load('art/buttons/arrow_right_regular.png')
arrow_r_h_img = pygame.image.load('art/buttons/arrow_right_hover.png')
arrow_l_r_img = pygame.image.load('art/buttons/arrow_left_regular.png')
arrow_l_h_img = pygame.image.load('art/buttons/arrow_left_hover.png')

buy_r_img = pygame.image.load('art/buttons/buy_regular.png')
buy_h_img = pygame.image.load('art/buttons/buy_hover.png')

sell_r_img = pygame.image.load('art/buttons/sell_regular.png')
sell_h_img = pygame.image.load('art/buttons/sell_hover.png')

max_r_img = pygame.image.load('art/buttons/max_regular.png')
max_h_img = pygame.image.load('art/buttons/max_hover.png')

min_r_img = pygame.image.load('art/buttons/min_regular.png')
min_h_img = pygame.image.load('art/buttons/min_hover.png')

# Shipyard Menu Buttons
back_r_img = pygame.image.load('art/buttons/back_regular.png')
back_h_img = pygame.image.load('art/buttons/back_hover.png')
buy_cog_r_img = pygame.image.load('art/buttons/buy_cog_regular.png')
buy_cog_h_img = pygame.image.load('art/buttons/buy_cog_hover.png')
buy_carrack_r_img = pygame.image.load('art/buttons/buy_carrack_regular.png')
buy_carrack_h_img = pygame.image.load('art/buttons/buy_carrack_hover.png')
buy_blockade_runner_r_img = pygame.image.load(
    'art/buttons/buy_blockade_runner_regular.png')
buy_blockade_runner_h_img = pygame.image.load(
    'art/buttons/buy_blockade_runner_hover.png')

# Calendar Menu Buttons
pause_toggle_r_img = pygame.image.load('art/buttons/pause_toggle_regular.png')
pause_toggle_h_img = pygame.image.load('art/buttons/pause_toggle_hover.png')

faster_r_img = pygame.image.load('art/buttons/faster_regular.png')
faster_h_img = pygame.image.load('art/buttons/faster_hover.png')

slower_r_img = pygame.image.load('art/buttons/slower_regular.png')
slower_h_img = pygame.image.load('art/buttons/slower_hover.png')

# MiniMap Buttons
recenter_r_img = pygame.image.load('art/buttons/recenter_regular.png')
recenter_h_img = pygame.image.load('art/buttons/recenter_hover.png')

button_images = [leave_r_img,
                 leave_h_img,
                 market_r_img,
                 market_h_img,
                 cancel_r_img,
                 cancel_h_img,
                 done_r_img,
                 done_h_img,
                 move_r_img,
                 move_h_img,
                 enter_city_r_img,
                 enter_city_h_img,
                 tile_info_r_img,
                 tile_info_h_img,
                 x_button_r_img,
                 x_button_h_img,
                 arrow_u_r_img,
                 arrow_u_h_img,
                 arrow_d_r_img,
                 arrow_d_h_img,
                 arrow_r_r_img,
                 arrow_r_h_img,
                 arrow_l_r_img,
                 arrow_l_h_img,
                 buy_r_img,
                 buy_h_img,
                 sell_r_img,
                 sell_h_img,
                 max_r_img,
                 max_h_img,
                 min_r_img,
                 min_h_img,
                 pause_toggle_r_img,
                 pause_toggle_h_img,
                 faster_r_img,
                 faster_h_img,
                 slower_r_img,
                 slower_h_img,
                 recenter_r_img,
                 recenter_h_img]

proc_button_left_edge_hover = pygame.image.load("art/buttons/button_left_edge_hover.png")
proc_button_right_edge_hover = pygame.image.load("art/buttons/button_right_edge_hover.png")
proc_button_center_hover = pygame.image.load("art/buttons/button_center_hover.png")

proc_button_left_edge_regular = pygame.image.load("art/buttons/button_left_edge_regular.png")
proc_button_right_edge_regular = pygame.image.load("art/buttons/button_right_edge_regular.png")
proc_button_center_regular = pygame.image.load("art/buttons/button_center_regular.png")

for img in button_images:
    img.set_colorkey(util.colors.key)
    img = img.convert_alpha()


def do_nothing(args):
    pass


class Button(object):
    def __init__(self, regular_image, hover_image, on_click, x=0, y=0):

        self.regular = regular_image
        self.hover = hover_image
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.regular
        self.sprite.rect = self.sprite.image.get_rect()
        self.click = on_click
        self.sprite.rect.x = x
        self.sprite.rect.y = y


def generate_button_images(button_text, button_font=None):
    if button_font is None:
        button_font = pygame.font.SysFont('Calibri', 16, True, False)
    button_stamp = button_font.render(button_text, True, util.colors.light_gray)
    button_width = button_stamp.get_width() + 14
    center_spacing = button_width - 18
    regular_img = pygame.Surface([button_width, 30])
    hover_img = pygame.Surface([button_width, 30])
    regular_img.blit(proc_button_left_edge_regular, [0, 0])
    regular_img.blit(proc_button_right_edge_regular, [button_width - 9, 0])
    hover_img.blit(proc_button_left_edge_hover, [0, 0])
    hover_img.blit(proc_button_right_edge_hover, [button_width - 9, 0])
    for ii in range(center_spacing):
        regular_img.blit(proc_button_center_regular, [9 + ii, 0])
        hover_img.blit(proc_button_center_hover, [9 + ii, 0])
    regular_img.blit(button_stamp, [7, 8])
    hover_img.blit(button_stamp, [7, 8])
    return regular_img, hover_img


class Menu(object):
    def __init__(self, game_state):
        self.open = True
        self.dragging = False
        self.drag_offset = None
        self.player = game_state.player
        self.screen = game_state.screen
        self.active_map = game_state.active_map
        self.screen_width = game_state.screen_width
        self.screen_height = game_state.screen_height
        self.game_state = game_state
        self.cached_image = pygame.Surface([0, 0])

    def render_buttons(self, pos):
        mouse_pos = (pos[0] - self.background_pane.rect.x,
                     pos[1] - self.background_pane.rect.y)
        for button in self.buttons:
            if util.check_if_inside(button.sprite.rect.x,
                                    button.sprite.rect.right,
                                    button.sprite.rect.y,
                                    button.sprite.rect.bottom,
                                    mouse_pos):
                button.sprite.image = button.hover
            else:
                button.sprite.image = button.regular
            self.screen.blit(button.sprite.image,
                             [button.sprite.rect.x, button.sprite.rect.y])

    def drag(self, pos):
        if not self.dragging:
            return

        if not self.drag_offset:
            x = self.background_pane.rect.x - pos[0]
            y = self.background_pane.rect.y - pos[1]
            self.drag_offset = (x, y)
        self.background_pane.rect.x = pos[0] + self.drag_offset[0]
        self.background_pane.rect.y = pos[1] + self.drag_offset[1]

    def update_last_pos(self):
        pass

    def keydown_handler(self, event, key):
        pass

    def keyup_handler(self, event, key):
        pass

    def render_decals(self, pos):
        pass

    def get_interaction(self, event, pos):
        if util.check_if_inside(
            self.background_pane.rect.left,
            self.background_pane.rect.right,
            self.background_pane.rect.top,
            self.background_pane.rect.bottom,
                pos):
            return True
        return False

    def mouse_release_handler(self, event, pos):
        self.dragging = False
        self.drag_offset = None

    def mouse_click_handler(self, event, pos):
        mouse_pos = (pos[0] - self.background_pane.rect.x,
                     pos[1] - self.background_pane.rect.y)
        for button in self.buttons:
            if util.check_if_inside(
                button.sprite.rect.x,
                button.sprite.rect.right,
                button.sprite.rect.y,
                button.sprite.rect.bottom,
                    mouse_pos):
                button.click()

    def event_handler(self, event, pos):
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_click_handler(event, pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_release_handler(event, pos)
        elif event.type == pygame.KEYDOWN:
            self.keydown_handler(event, event.key)
        elif event.type == pygame.KEYUP:
            self.keyup_handler(event, event.key)

    def render_onscreen_cache(self, pos):
        self.cached_image = pygame.Surface(
            [self.background_pane.image.get_width(),
             self.background_pane.image.get_height()])
        self.render_buttons(pos)
        self.cached_image.blit(self.background_pane.image, [0, 0])
        for button in self.buttons:
            self.cached_image.blit(button.sprite.image,
                                   [button.sprite.rect.x, button.sprite.rect.y])
        self.render_decals(pos)


class MainMenu(Menu):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = art.main_menu
        self.background_pane.rect = self.background_pane.image.get_rect()
        x_origin = (self.screen.get_width() / 2 -
                    self.background_pane.image.get_width() / 2)
        y_origin = 0
        self.background_pane.rect.x = x_origin
        self.background_pane.rect.y = y_origin

        def new_game_click():
            self.open = False

        def load_game_click():
            pass

        def options_click():
            new_options_menu = OptionsMenu(self.game_state)
            self.game_state.active_menus.insert(0, new_options_menu)

        def quit_game_click():
            pygame.display.quit()
            pygame.quit()

        mm_font = pygame.font.SysFont('Gabriola', 16, True, False)
        new_game_r_img, new_game_h_img = generate_button_images("New Game", mm_font)
        load_game_r_img, load_game_h_img = generate_button_images("Load Game", mm_font)
        options_r_img, options_h_img = generate_button_images("Options", mm_font)
        quit_game_r_img, quit_game_h_img = generate_button_images("Quit", mm_font)

        new_game = Button(
            new_game_r_img,
            new_game_h_img,
            new_game_click,
            math.floor(self.background_pane.image.get_width() / 2 -
                       new_game_r_img.get_width() / 2),
            300)
        load_game = Button(
            load_game_r_img,
            load_game_h_img,
            load_game_click,
            math.floor(self.background_pane.image.get_width() / 2 -
                       load_game_r_img.get_width() / 2),
            360)
        options = Button(
            options_r_img,
            options_h_img,
            options_click,
            math.floor(self.background_pane.image.get_width() / 2 -
                       options_r_img.get_width() / 2),
            420)
        quit_game = Button(
            quit_game_r_img,
            quit_game_h_img,
            quit_game_click,
            math.floor(self.background_pane.image.get_width() / 2 -
                       quit_game_r_img.get_width() / 2),
            480)
        self.buttons = [new_game, load_game, options, quit_game]


class OptionsMenu(Menu):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = art.options_menu
        self.background_pane.rect = self.background_pane.image.get_rect()
        x_origin = (self.screen.get_width() / 2 -
                    self.background_pane.image.get_width() / 2)
        y_origin = (
            game_state.screen_height / 2 - self.background_pane.image.get_height() / 2)
        self.background_pane.rect.x = x_origin
        self.background_pane.rect.y = y_origin

        def load_game_click():
            self.open = False
            saved_state = pickle.load(open("saves/save_1.p", "rb"))
            self.game_state.load_external_state(saved_state)
            mini_map = MiniMap(self.game_state)
            calendar_menu = CalendarMenu(self.game_state)
            self.game_state.active_menus.append(mini_map)
            self.game_state.active_menus.append(calendar_menu)
            self.game_state.active_menus.insert(0, self)

        def save_game_click():
            if self.game_state.active_map is None:
                return
            save_string = "save_1"
            self.game_state.clock = None
            self.game_state.active_menus = []

            pickle.dump(game_state, open("saves/{0}.p".format(save_string), "wb"))
            self.game_state.clock = pygame.time.Clock()
            mini_map = MiniMap(self.game_state)
            calendar_menu = CalendarMenu(self.game_state)
            self.game_state.active_menus.append(mini_map)
            self.game_state.active_menus.append(calendar_menu)
            self.game_state.active_menus.insert(0, self)

        def go_back_click():
            self.open = False

        def quit_main_click():
            pygame.display.quit()
            pygame.quit()

        def exit_to_desktop_click():
            pygame.display.quit()
            pygame.quit()

        load_game_r_img, load_game_h_img = generate_button_images("Load Game")
        save_game_r_img, save_game_h_img = generate_button_images("Save Game")
        go_back_r_img, go_back_h_img = generate_button_images("Back")
        quit_main_r_img, quit_main_h_img = generate_button_images("Quit to Main Menu")
        exit_r_img, exit_h_img = generate_button_images("Exit to Desktop")

        load_game = Button(
            load_game_r_img,
            load_game_h_img,
            load_game_click,
            math.floor(self.background_pane.image.get_width() / 2 -
                       load_game_r_img.get_width() / 2),
            200)

        save_game = Button(
            save_game_r_img,
            save_game_h_img,
            save_game_click,
            math.floor(self.background_pane.image.get_width() / 2 -
                       save_game_r_img.get_width() / 2),
            240)

        go_back = Button(
            go_back_r_img,
            go_back_h_img,
            go_back_click,
            math.floor(self.background_pane.image.get_width() / 2 -
                       go_back_r_img.get_width() / 2),
            280)
        quit_game = Button(
            quit_main_r_img,
            quit_main_h_img,
            quit_main_click,
            math.floor(self.background_pane.image.get_width() / 2 -
                       quit_main_r_img.get_width() / 2),
            320)
        exit = Button(
            exit_r_img,
            exit_h_img,
            exit_to_desktop_click,
            math.floor(self.background_pane.image.get_width() / 2 -
                       exit_r_img.get_width() / 2),
            360)
        self.buttons = [load_game, save_game, go_back, quit_game, exit]


class ConsoleWindow(Menu):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = pygame.Surface([400, 400])
        self.background_pane.image.fill(util.colors.black)
        self.background_pane.image.set_alpha(75)
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = game_state.screen_width / 2 - 200
        self.background_pane.rect.y = game_state.screen_height / 2 - 200

        self.current_line = ""

        def set_draw_routes(args):
            if args[0].lower() == "true" or args[0].lower() == "false":
                self.game_state.draw_routes = (args[0].lower() == "true")
                self.game_state.console_log.append(
                    'Draw Routes set to {0}'.format(args[0].lower()))

        def set_infinite_speed(args):
            if args[0].lower() == "true" or args[0].lower() == "false":
                self.game_state.infinite_speed = (args[0].lower() == "true")
                self.game_state.console_log.append(
                    'Infinite Speed set to {0}'.format(args[0].lower()))

        def set_draw_borders(args):
            if args[0].lower() == "true" or args[0].lower() == "false":
                self.game_state.draw_borders = (args[0].lower() == "true")
                self.game_state.console_log.append(
                    'Draw Borders set to {0}'.format(args[0].lower()))

        self.console_functions = {"draw_routes": set_draw_routes,
                                  "infinite_speed": set_infinite_speed,
                                  "draw_borders": set_draw_borders}
        self.buttons = []

    def keydown_handler(self, event, key):
        if key is pygame.K_RETURN:
            self.game_state.console_log.append(self.current_line)
            console_args = self.current_line.split()
            command = console_args[0]
            self.console_functions.get(command, do_nothing)(console_args[1:])
            self.current_line = ''
        elif key == pygame.K_F1:
            self.open = False
        elif key is pygame.K_BACKSPACE:
            self.current_line = self.current_line[:-1]
        else:
            self.current_line = self.current_line + event.unicode

    def render_decals(self, pos):
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        current_line_stamp = header_font.render(
            self.current_line,
            True,
            util.colors.white)
        self.cached_image.blit(
            current_line_stamp,
            [2, self.background_pane.rect.height - 20])
        for n in range(min(len(self.game_state.console_log), 9)):
            console_log_line = self.game_state.console_log[-(n + 1)]
            console_log_line_stamp = header_font.render(
                console_log_line,
                True,
                util.colors.light_gray)
            self.cached_image.blit(
                console_log_line_stamp,
                [2, self.background_pane.rect.height - (20 + (n + 1) * 20)])

    def render_onscreen_cache(self, pos):
        self.cached_image = pygame.Surface(
            [self.background_pane.image.get_width(),
             self.background_pane.image.get_height()])
        self.render_buttons(pos)
        self.cached_image.fill(util.colors.key)
        self.cached_image.set_colorkey(util.colors.key)
        self.cached_image = self.cached_image.convert_alpha()
        self.cached_image.blit(self.background_pane.image, [0, 0])
        for button in self.buttons:
            self.cached_image.blit(button.sprite.image,
                                   [button.sprite.rect.x, button.sprite.rect.y])
        self.render_decals(pos)


class ViewCity(Menu):
    def __init__(self, game_state, city, width=400, height=400):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        x = game_state.active_map.tile_display_layer.image.get_width() / 2
        city_tiles_image = pygame.Surface([400, 400])
        city_tiles_image.fill((32, 61, 82))
        print(city.column, city.row)
        city_pxy = util.get_screen_coords(city.column, city.row)
        print(city_pxy)
        city_tiles_image.blit(
            game_state.active_map.tile_display_layer.image,
            (0, 0), [city_pxy[0] + x - width / 2, city_pxy[1] - height / 2,
                     width, height])
        city_tiles_image.blit(
            game_state.active_map.terrain_display_layer.image,
            (0, 0), [city_pxy[0] + x - width / 2, city_pxy[1] - height / 2,
                     width, height])
        city_tiles_image.blit(
            game_state.active_map.resource_display_layer.image,
            (0, 0), [city_pxy[0] + x - width / 2, city_pxy[1] - height / 2,
                     width, height])
        city_tiles_image.blit(
            game_state.active_map.building_display_layer.image,
            (0, 0), [city_pxy[0] + x - width / 2, city_pxy[1] - height / 2,
                     width, height])
        province_border = city.province_border
        adjusted_points = []
        print(province_border)
        for point in province_border:
            adjusted_points.append(
                (point[0] + x - city_pxy[0] + width / 2,
                 point[1] - city_pxy[1] + height / 2))
        pygame.draw.aalines(city_tiles_image, util.colors.red, True, adjusted_points)

        self.background_pane.image = pygame.Surface([420, 420])
        self.background_pane.image.fill((32, 61, 82))
        self.background_pane.image.blit(city_tiles_image, [10, 18])
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = (
            game_state.screen_width / 2 - self.background_pane.image.get_width() / 2)
        self.background_pane.rect.y = (
            game_state.screen_height / 2 - self.background_pane.image.get_height() / 2)

        def x_click():
            self.open = False

        def dragbar_click():
            self.dragging = True

        x_button = Button(
            x_button_r_img,
            x_button_h_img,
            x_click,
            self.background_pane.image.get_width() - 22,
            10)

        dragbar_r_img = pygame.Surface([self.background_pane.image.get_width() - 2, 9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(
            dragbar_r_img,
            dragbar_r_img,
            dragbar_click,
            1,
            1)

        self.buttons = [x_button, dragbar]


class ShipStatus(Menu):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = art.ship_status_screen
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = (
            game_state.screen_width / 2 - self.background_pane.image.get_width() / 2)
        self.background_pane.rect.y = (
            game_state.screen_height / 2 - self.background_pane.image.get_height() / 2)

        def x_click():
            self.open = False

        def dragbar_click():
            self.dragging = True

        x_button = Button(
            x_button_r_img,
            x_button_h_img,
            x_click,
            self.background_pane.image.get_width() - 22,
            10)

        dragbar_r_img = pygame.Surface([self.background_pane.image.get_width() - 2, 9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(
            dragbar_r_img,
            dragbar_r_img,
            dragbar_click,
            1,
            1)

        self.buttons = [x_button, dragbar]

    def render_decals(self, pos):
        ship = self.game_state.player.ship
        header_font = pygame.font.SysFont('Calibri', 14, True, False)

        hull_class_stamp = header_font.render(
            "{0}".format(ship.hull_class),
            True,
            util.colors.yellow)  # 14, 32
        speed_stamp = header_font.render(
            "{0}".format(ship.speed),
            True,
            util.colors.yellow)  # 12, 82
        attack_stamp = header_font.render(
            "{0}".format(ship.attack),
            True,
            util.colors.yellow)  # 82, 82
        defense_stamp = header_font.render(
            "{0}".format(str(ship.defense)),
            True,
            util.colors.yellow)  # 152, 82
        crew_stamp = header_font.render(
            "{0} / {1}".format(str(ship.crew_cap), str(ship.crew_cap)),
            True,
            util.colors.yellow)  # 12, 138
        upkeep_stamp = header_font.render(
            "₴{0}".format(str(ship.upkeep)),
            True,
            util.colors.yellow)  # 142, 136
        cargo_cap_stamp = header_font.render(
            "{0} / {1}".format(str(ship.cargo_cap), str(ship.cargo_cap)),
            True,
            util.colors.yellow)  # 46, 182
        self.cached_image.blit(hull_class_stamp, [14, 32])
        self.cached_image.blit(speed_stamp, [12, 82])
        self.cached_image.blit(attack_stamp, [82, 82])
        self.cached_image.blit(defense_stamp, [152, 82])
        self.cached_image.blit(crew_stamp, [12, 138])
        self.cached_image.blit(upkeep_stamp, [142, 138])
        self.cached_image.blit(cargo_cap_stamp, [46, 182])
        self.cached_image.blit(
            pygame.transform.scale(ship.image, (300, 300)), [145, -100])


class ContextMenu(Menu):
    def __init__(self, game_state, pos, tile):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = context_menu
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = pos[0]
        self.background_pane.rect.y = pos[1]
        self.tile = tile

        def move_click():
            if tile.biome in (
                ["ocean",
                 "sea",
                 "shallows",
                 "lake"]) or tile.terrain == "river":
                game_state.player.target_tile = tile
                new_path = game_state.player.check_path_to_target()
                if new_path is not None:
                    game_state.player.set_path(new_path)
                else:
                    cannot_move_popup = ImpassablePopup(game_state)
                    game_state.active_menus = (
                        [cannot_move_popup] + game_state.active_menus)
                self.open = False
            else:
                cannot_move_popup = ImpassablePopup(game_state)
                game_state.active_menus = [cannot_move_popup] + game_state.active_menus
                self.open = False

        def enter_city_click():
            new_city_menu = CityMenu(game_state, self.tile.city)
            game_state.active_menus = [new_city_menu] + game_state.active_menus
            self.open = False

        def tile_info_click():
            new_tile_info_pane = TileInfoPane(game_state, pos, tile)
            game_state.active_menus = [new_tile_info_pane] + game_state.active_menus
            self.open = False

        def cancel_click():
            self.open = False

        move_button = Button(
            move_r_img,
            move_h_img,
            move_click,
            5,
            25)

        enter_city_button = Button(
            enter_city_r_img,
            enter_city_h_img,
            enter_city_click,
            78,
            25)

        tile_info_button = Button(
            tile_info_r_img,
            tile_info_h_img,
            tile_info_click,
            151,
            25)

        cancel_button = Button(
            cancel_r_img,
            cancel_h_img,
            cancel_click,
            224,
            25)
        self.buttons = [move_button, tile_info_button, cancel_button]
        player_tile = self.game_state.active_map.game_tile_rows[game_state.player.ship.row][game_state.player.ship.column]
        if (self.tile.city and
            (self.tile in
             util.get_adjacent_movement_tiles(player_tile, game_state.active_map))):
            self.buttons.append(enter_city_button)

    def render_decals(self, pos):
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        header_text = "{0} {1}".format(self.tile.biome, self.tile.terrain)
        if self.tile.city:
            header_text = "{0}".format(self.tile.city.name)
        header_stamp = header_font.render(header_text, True, util.colors.white)
        self.cached_image.blit(header_stamp, [5, 5])


class ImpassablePopup(Menu):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = impassable_popup_pane
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = (
            (self.game_state.screen.get_width() / 2) -
            (self.background_pane.image.get_width() / 2))
        self.background_pane.rect.y = (
            (self.game_state.screen.get_height() / 2) -
            (self.background_pane.image.get_height() / 2))

        def ok_click():
            self.open = False

        def dragbar_click():
            self.dragging = True

        ok_button = Button(
            ok_r_img,
            ok_h_img,
            ok_click,
            self.background_pane.image.get_width() / 2 - 28,
            56)

        dragbar_r_img = pygame.Surface(
            [self.background_pane.image.get_width() - 2,
             9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(
            dragbar_r_img,
            dragbar_r_img,
            dragbar_click,
            1,
            1)

        self.buttons = [ok_button, dragbar]


class TileInfoPane(Menu):
    def __init__(self, game_state, pos, tile):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = tile_info_pane
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = pos[0]
        self.background_pane.rect.y = pos[1]
        self.tile = tile

        def ok_click():
            self.open = False

        def dragbar_click():
            self.dragging = True

        ok_button = Button(
            ok_r_img,
            ok_h_img,
            ok_click,
            10,
            270)

        dragbar_r_img = pygame.Surface(
            [self.background_pane.image.get_width() - 2,
             9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(
            dragbar_r_img,
            dragbar_r_img,
            dragbar_click,
            1,
            1)

        self.buttons = [ok_button, dragbar]

    def render_decals(self, pos):
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        coordinates_text = "{0}, {1}".format(self.tile.column, self.tile.row)
        biome_text = self.tile.biome
        terrain_text = self.tile.terrain
        resource_text = "None"
        if self.tile.resource:
            resource_text = self.tile.resource
        city_text = "None"
        if self.tile.city:
            city_text = self.tile.city.name
        coordinates_stamp = header_font.render(coordinates_text, True, util.colors.white)
        biome_stamp = header_font.render(biome_text, True, util.colors.white)
        terrain_stamp = header_font.render(terrain_text, True, util.colors.white)
        resource_stamp = header_font.render(resource_text, True, util.colors.white)
        city_stamp = header_font.render(city_text, True, util.colors.white)
        water_flux_stamp = header_font.render(
            "{0}, {1}, {2}".format(self.tile.water_source[0],
                                   self.tile.water_source[1],
                                   self.tile.water_flux[2]),
            True,
            util.colors.white)

        self.cached_image.blit(coordinates_stamp, [8, 73])
        self.cached_image.blit(biome_stamp, [8, 115])
        self.cached_image.blit(water_flux_stamp, [100, 115])
        self.cached_image.blit(terrain_stamp, [8, 156])
        if self.tile.resource:
            self.cached_image.blit(
                art.resource_images[self.tile.resource][0],
                [5 + resource_stamp.get_width(), 200 - 20])
        self.cached_image.blit(resource_stamp, [8, 200])
        self.cached_image.blit(city_stamp, [8, 245])


class CityMenu(Menu):
    def __init__(self, game_state, city):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = city_menu_pane
        self.background_pane.image.blit(city.portrait_img, [5, 14])
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = (
            (self.game_state.screen.get_width() / 2) -
            (self.background_pane.image.get_width() / 2))
        self.background_pane.rect.y = (
            (self.game_state.screen.get_height() / 2) -
            (self.background_pane.image.get_height() / 2))
        self.city = city

        def leave_click():
            self.open = False

        def market_click():
            new_market_menu = MarketMenu(game_state, city)
            game_state.clear_menutype([MarketMenu])
            game_state.active_menus = [new_market_menu] + game_state.active_menus
            self.open = False

        def tavern_click():
            pass

        def shipyard_click():
            new_shipyard_menu = ShipyardMenu(game_state, city)
            game_state.clear_menutype([ShipyardMenu])
            game_state.active_menus = [new_shipyard_menu] + game_state.active_menus
            self.open = False

        def city_hall_click():
            new_city_hall_menu = CityHallMenu(game_state, city)
            game_state.clear_menutype([CityHallMenu])
            game_state.active_menus = [new_city_hall_menu] + game_state.active_menus
            self.open = False

        def dragbar_click():
            self.dragging = True

        leave_button = Button(
            leave_r_img,
            leave_h_img,
            leave_click,
            5,
            175)

        market_button = Button(
            market_r_img,
            market_h_img,
            market_click,
            5,
            140)

        tavern_button = Button(
            tavern_r_img,
            tavern_h_img,
            tavern_click,
            80,
            140)

        shipyard_button = Button(
            shipyard_r_img,
            shipyard_h_img,
            shipyard_click,
            80,
            175)

        city_hall_r_img, city_hall_h_img = generate_button_images("City Hall")

        city_hall_button = Button(
            city_hall_r_img,
            city_hall_h_img,
            city_hall_click,
            155,
            140)

        dragbar_r_img = pygame.Surface(
            [self.background_pane.image.get_width() - 2,
             9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(
            dragbar_r_img,
            dragbar_r_img,
            dragbar_click,
            1,
            1)

        self.buttons = [leave_button,
                        market_button,
                        tavern_button,
                        shipyard_button,
                        city_hall_button,
                        dragbar]

    def render_decals(self, pos):
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        city_name_text = "{0}".format(self.city.name)
        city_name_stamp = header_font.render(city_name_text, True, util.colors.white)
        self.cached_image.blit(
            city_name_stamp,
            [self.background_pane.image.get_width() / 2, 15])


class MarketMenu(Menu):
    def __init__(self, game_state, city):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = market_menu_pane
        self.background_pane.rect = self.background_pane.image.get_rect()
        x_origin = (self.screen.get_width() / 2 -
                    self.background_pane.image.get_width() / 2)
        y_origin = (self.screen.get_height() / 2 -
                    self.background_pane.image.get_height() / 2)
        self.background_pane.rect.x = x_origin
        self.background_pane.rect.y = y_origin

        self.city = city
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        self.name_stamp = header_font.render("{0} Market".format(city.name),
                                             True,
                                             (255, 255, 255))

        self.display_cache = {"market commodities list": [],
                              "cargo commodities list": [],
                              "market list top": 0,
                              "cargo list top": 0,
                              "market visible items": [],
                              "cargo visible items": [],
                              "market selected": 0,
                              "cargo selected": 0,
                              "market selection box": pygame.sprite.Sprite(),
                              "cargo selection box": pygame.sprite.Sprite(),
                              "cargo cap": "0 / 0"}

        self.update_display_cache()

        def x_click():
            self.open = False

        def sell_click():
            artikel_name = self.display_cache["cargo visible items"][self.display_cache["cargo selected"]]
            sell_quantity_popup = QuantityMenu(
                self.game_state,
                self.player,
                self.city,
                artikel_name,
                "sale")
            game_state.active_menus = [sell_quantity_popup] + game_state.active_menus

            self.update_display_cache()

        def buy_click():
            artikel_name = self.display_cache["market visible items"][self.display_cache["market selected"]]
            buy_quantity_popup = QuantityMenu(
                self.game_state,
                self.player,
                self.city,
                artikel_name,
                "purchase")
            game_state.clear_menutype([QuantityMenu])
            game_state.active_menus = [buy_quantity_popup] + game_state.active_menus

            self.update_display_cache()

        def market_up_click():
            if self.display_cache["market list top"] > 0:
                self.display_cache["market list top"] -= 1
                self.update_display_cache()

        def market_down_click():
            if (self.display_cache["market list top"] <
                    len(self.display_cache["market commodities list"]) - 1):
                self.display_cache["market list top"] += 1
                self.update_display_cache()

        def cargo_up_click():
            if self.display_cache["cargo list top"] > 0:
                self.display_cache["cargo list top"] -= 1
                self.update_display_cache()

        def cargo_down_click():
            if (self.display_cache["cargo list top"] <
                    len(self.display_cache["cargo commodities list"]) - 1):
                self.display_cache["cargo list top"] += 1
                self.update_display_cache()

        def back_click():
            new_city_menu = CityMenu(game_state, self.city)
            game_state.active_menus = [new_city_menu] + game_state.active_menus
            self.open = False

        def dragbar_click():
            self.dragging = True

        dragbar_r_img = pygame.Surface([self.background_pane.image.get_width() - 2, 9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(dragbar_r_img,
                         dragbar_r_img,
                         dragbar_click,
                         1,
                         1)

        x_button = Button(x_button_r_img,
                          x_button_h_img,
                          x_click,
                          self.background_pane.image.get_width() - 22,
                          13)

        back_button = Button(
            back_r_img,
            back_h_img,
            back_click,
            self.background_pane.image.get_width() - 44,
            13)

        sell_button = Button(sell_r_img,
                             sell_h_img,
                             sell_click,
                             432,
                             410)

        buy_button = Button(buy_r_img,
                            buy_h_img,
                            buy_click,
                            14,
                            410)

        market_up_arrow = Button(arrow_u_r_img,
                                 arrow_u_h_img,
                                 market_up_click,
                                 14,
                                 58)

        market_down_arrow = Button(arrow_d_r_img,
                                   arrow_d_h_img,
                                   market_down_click,
                                   14,
                                   385)

        cargo_up_arrow = Button(arrow_u_r_img,
                                arrow_u_h_img,
                                cargo_up_click,
                                466,
                                58)

        cargo_down_arrow = Button(arrow_d_r_img,
                                  arrow_d_h_img,
                                  cargo_down_click,
                                  466,
                                  385)

        self.buttons = [x_button,
                        back_button,
                        sell_button,
                        buy_button,
                        market_up_arrow,
                        market_down_arrow,
                        cargo_up_arrow,
                        cargo_down_arrow,
                        dragbar]

    def update_display_cache(self):
        self.display_cache["silver"] = self.player.silver
        current_cargo = 0
        for artikel_name, artikel_quantity in self.player.ship.cargo.items():
            current_cargo += artikel_quantity
        self.display_cache["cargo cap"] = "{0} / {1}".format(
            str(current_cargo), str(self.player.ship.cargo_cap))
        self.display_cache["market artikels list"] = []
        for artikel_name, artikel_quantity, in self.city.supply.items():
            if artikel_quantity > 0:
                self.display_cache["market artikels list"].append(artikel_name)
        self.display_cache["cargo artikels list"] = []
        for artikel_name, artikel_quantity, in self.player.ship.cargo.items():
            if artikel_quantity > 0:
                self.display_cache["cargo artikels list"].append(artikel_name)

        if self.display_cache["market selected"] > len(self.display_cache["market artikels list"]) - 1:
            self.display_cache["market selected"] -= 1
        if self.display_cache["cargo selected"] > len(self.display_cache["cargo artikels list"]) - 1:
            self.display_cache["cargo selected"] -= 1
        market_list = self.display_cache["market artikels list"]
        self.display_cache["market visible items"] = market_list[self.display_cache["market list top"]:self.display_cache["market list top"] + 20]
        cargo_list = self.display_cache["cargo artikels list"]
        self.display_cache["cargo visible items"] = cargo_list[self.display_cache["cargo list top"]:self.display_cache["cargo list top"] + 20]
        self.update_selection_boxes()

    def update_selection_boxes(self):
        box_y = 58 + ((
            self.display_cache["market selected"] -
            self.display_cache["market list top"]) * 14)
        self.display_cache["market selection box"].image = pygame.Rect(37,
                                                                       box_y,
                                                                       208,
                                                                       15)
        box_y = 58 + ((
            self.display_cache["cargo selected"] -
            self.display_cache["cargo list top"]) * 14)
        self.display_cache["cargo selection box"].image = pygame.Rect(252,
                                                                      box_y,
                                                                      208,
                                                                      15)

    def mouse_click_handler(self, event, pos):
        mouse_pos = (pos[0] - self.background_pane.rect.x,
                     pos[1] - self.background_pane.rect.y)
        for button in self.buttons:
            if util.check_if_inside(button.sprite.rect.x,
                                    button.sprite.rect.right,
                                    button.sprite.rect.y,
                                    button.sprite.rect.bottom,
                                    mouse_pos):
                button.click()
        count = 0
        spacer = 14
        for each in self.display_cache["market visible items"]:
            x1 = 37
            x2 = x1 + 170
            y1 = (58 + (count * spacer))
            y2 = y1 + 15
            if util.check_if_inside(x1, x2, y1, y2, mouse_pos):
                self.display_cache["market selected"] = count + self.display_cache["market list top"]
                self.update_display_cache()
            count += 1

        count = 0
        for each in self.display_cache["cargo visible items"]:
            x1 = 252
            x2 = x1 + 170
            y1 = (58 + (count * spacer))
            y2 = y1 + 15
            if util.check_if_inside(x1, x2, y1, y2, mouse_pos):
                self.display_cache["cargo selected"] = count + self.display_cache["cargo list top"]
                self.update_display_cache()
            count += 1

    def draw_selection_boxes(self):
        if self.display_cache["market list top"] <= self.display_cache["market selected"] <= self.display_cache["market list top"] + 21:
            pygame.draw.rect(
                self.cached_image,
                (255, 198, 13),
                self.display_cache["market selection box"].image,
                1)
        if self.display_cache["cargo list top"] <= self.display_cache["cargo selected"] <= self.display_cache["cargo list top"] + 21:
            pygame.draw.rect(
                self.cached_image,
                (255, 198, 13),
                self.display_cache["cargo selection box"].image,
                1)

    def render_decals(self, pos):
        left_margin = (
            (self.background_pane.image.get_width() / 2) -
            (self.name_stamp.get_width() / 2))
        self.update_display_cache()
        self.cached_image.blit(self.name_stamp, [left_margin, 12])
        small_font = pygame.font.SysFont("Calibri", 14, True, False)
        silver_stamp = small_font.render(
            "Silver: {0}".format(str(self.display_cache["silver"])),
            True,
            (255, 255, 255))
        self.cached_image.blit(silver_stamp, [3, 13])
        count = 0
        spacer = 14
        for artikel_name in self.display_cache["market visible items"]:
            artikel_name_stamp = small_font.render(
                artikel_name, True, (255, 255, 255))
            artikel_quantity_stamp = small_font.render(
                str(self.city.supply[artikel_name]), True, (255, 255, 255))
            artikel_price_stamp = small_font.render(
                str(self.city.purchase_price[artikel_name]), True, (200, 0, 0))

            self.cached_image.blit(artikel_quantity_stamp, [37,
                                                            60 + count * spacer])
            self.cached_image.blit(artikel_name_stamp, [90,
                                                        60 + count * spacer])
            self.cached_image.blit(artikel_price_stamp, [210,
                                                         60 + count * spacer])
            count += 1

        count = 0
        spacer = 14
        for artikel_name in self.display_cache["cargo visible items"]:
            if self.player.ship.cargo[artikel_name] > 0:
                artikel_name_stamp = small_font.render(
                    artikel_name, True, (255, 255, 255))
                artikel_quantity_stamp = small_font.render(
                    str(self.player.ship.cargo[artikel_name]), True, (255, 255, 255))
                artikel_price_stamp = small_font.render(
                    str(self.city.sell_price[artikel_name]), True, (0, 210, 0))
                self.cached_image.blit(artikel_quantity_stamp, [252,
                                                                60 + count * spacer])
                self.cached_image.blit(artikel_name_stamp, [305,
                                                            60 + count * spacer])
                self.cached_image.blit(artikel_price_stamp, [440,
                                                             60 + count * spacer])
                count += 1
        cargo_stamp = small_font.render(
            self.display_cache["cargo cap"],
            True,
            (255, 255, 255))
        self.cached_image.blit(cargo_stamp, [314, 448])
        self.draw_selection_boxes()


class ShipyardMenu(Menu):
    def __init__(self, game_state, city):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = art.shipyard_menu
        self.background_pane.image.blit(art.shipyard_portrait_img, [5, 14])
        self.background_pane.rect = self.background_pane.image.get_rect()
        x_origin = (self.screen.get_width() / 2 -
                    self.background_pane.image.get_width() / 2)
        y_origin = (self.screen.get_height() / 2 -
                    self.background_pane.image.get_height() / 2)
        self.background_pane.rect.x = x_origin
        self.background_pane.rect.y = y_origin
        self.city = city

        def dragbar_click():
            self.dragging = True

        def x_click():
            self.open = False

        def back_click():
            new_city_menu = CityMenu(game_state, self.city)
            game_state.active_menus = [new_city_menu] + game_state.active_menus
            self.open = False

        dragbar_r_img = pygame.Surface(
            [self.background_pane.image.get_width() - 2, 9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(
            dragbar_r_img,
            dragbar_r_img,
            dragbar_click,
            1,
            1)

        back_button = Button(
            back_r_img,
            back_h_img,
            back_click,
            self.background_pane.image.get_width() - 44,
            13)

        x_button = Button(
            x_button_r_img,
            x_button_h_img,
            x_click,
            self.background_pane.image.get_width() - 22,
            13)

        ship_purchase_buttons = []
        for i, ship_type in enumerate(self.city.ships_available):
            def procedural_button_click():
                pass
            ship_name = ship_type.hull_class
            procedural_r_img, procedural_h_img = generate_button_images(
                "Buy {0}".format(ship_name))

            procedural_button = Button(
                procedural_r_img,
                procedural_h_img,
                procedural_button_click,
                6,
                160 + ((1 + i) * 40))
            ship_purchase_buttons.append(procedural_button)

        self.buttons = [dragbar, back_button, x_button] + ship_purchase_buttons

    def render_decals(self, pos):
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        city_name_text = "{0} Shipyard".format(self.city.name)
        city_name_stamp = header_font.render(city_name_text, True, util.colors.white)
        self.cached_image.blit(
            city_name_stamp,
            [self.background_pane.image.get_width() / 2, 15])


class CityHallMenu(Menu):
    def __init__(self, game_state, city):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = art.shipyard_menu
        self.background_pane.image.blit(random.choice(art.city_hall_portraits), [5, 14])
        self.background_pane.rect = self.background_pane.image.get_rect()
        x_origin = (self.screen.get_width() / 2 -
                    self.background_pane.image.get_width() / 2)
        y_origin = (self.screen.get_height() / 2 -
                    self.background_pane.image.get_height() / 2)
        self.background_pane.rect.x = x_origin
        self.background_pane.rect.y = y_origin
        self.city = city

        def dragbar_click():
            self.dragging = True

        def x_click():
            self.open = False

        def back_click():
            new_city_menu = CityMenu(game_state, self.city)
            game_state.active_menus = [new_city_menu] + game_state.active_menus
            self.open = False

        dragbar_r_img = pygame.Surface(
            [self.background_pane.image.get_width() - 2, 9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(
            dragbar_r_img,
            dragbar_r_img,
            dragbar_click,
            1,
            1)

        back_button = Button(
            back_r_img,
            back_h_img,
            back_click,
            self.background_pane.image.get_width() - 44,
            13)

        x_button = Button(
            x_button_r_img,
            x_button_h_img,
            x_click,
            self.background_pane.image.get_width() - 22,
            13)

        self.buttons = [dragbar, back_button, x_button]

    def render_decals(self, pos):
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        data_font = pygame.font.SysFont('Calibri', 14, True, False)
        city_name_text = "{0} City Hall".format(self.city.name)
        city_name_stamp = header_font.render(city_name_text, True, util.colors.white)
        city_size_stamp = data_font.render(
            "Population: {0},000".format(self.city.size),
            True, util.colors.white)
        self.cached_image.blit(
            city_name_stamp,
            [self.background_pane.image.get_width() / 2, 15])
        self.cached_image.blit(
            city_size_stamp,
            [6, 160])


class QuantityMenu(Menu):
    def __init__(self, game_state, player, city, artikel_name, transaction_type):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = quantity_popup
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = (
            self.screen.get_width() / 2 - self.background_pane.image.get_width() / 2)
        self.background_pane.rect.y = (
            (self.screen.get_height() / 2) - self.background_pane.image.get_height() / 2)
        self.artikel_name = artikel_name
        self.artikel_quantity = 0
        self.max_quantity = 0
        self.transaction_type = transaction_type
        self.city = city
        if self.transaction_type == "sale":
            self.max_quantity = self.player.ship.cargo[self.artikel_name]
        else:
            self.max_quantity = self.city.supply[self.artikel_name]
        self.step = 1

        self.transaction_modifiers = {
            "purchase": self.city.purchase_price[self.artikel_name],
            "sale": self.city.sell_price[self.artikel_name]}
        self.transaction_colors = {
            "purchase": (200, 0, 0),
            "sale": (0, 210, 0)}
        header_font = pygame.font.SysFont("Calibri", 18, True, False)

        self.display_cache = {
            "artikel quantity": self.artikel_quantity,
            "artikel max": self.max_quantity,
            "artikel name": header_font.render(
                self.artikel_name,
                True,
                (255, 255, 255))}

        self.update_display_cache()

        def quantity_up_click():
            cargo_margin = 0  # remaining empty space in the player's ship
            cargo_margin += self.player.ship.cargo_cap
            loaded_cargo = 0
            for artikel_name, quantity in self.player.ship.cargo.items():
                loaded_cargo += quantity
            cargo_margin -= loaded_cargo
            if self.artikel_quantity < self.max_quantity:
                self.artikel_quantity = min(self.artikel_quantity + self.step,
                                            self.max_quantity)
            self.update_display_cache()

        def quantity_down_click():
            if self.artikel_quantity > 0:
                self.artikel_quantity = max(self.artikel_quantity - self.step,
                                            0)
            self.update_display_cache()

        def max_click():
            self.artikel_quantity = self.max_quantity
            self.update_display_cache()

        def min_click():
            self.artikel_quantity = 0
            self.update_display_cache()

        def done_click():
            tcost = (
                self.artikel_quantity *
                self.transaction_modifiers[self.transaction_type])
            if self.transaction_type == "purchase":
                if self.player.silver >= tcost:
                    current_cargo = 0
                    for artikel_id, quantity in self.player.ship.cargo.items():
                        current_cargo += quantity
                    if current_cargo + self.artikel_quantity <= self.player.ship.cargo_cap:
                        self.city.increment_supply(artikel_name, -self.artikel_quantity)
                        self.player.silver -= (
                            self.artikel_quantity *
                            self.city.purchase_price[artikel_name])
                        if artikel_name in self.player.ship.cargo:
                            self.player.ship.cargo[artikel_name] += self.artikel_quantity
                        else:
                            self.player.ship.cargo[artikel_name] = self.artikel_quantity
                        self.open = False
            elif self.transaction_type == "sale":
                self.player.ship.cargo[self.artikel_name] -= self.artikel_quantity
                self.player.silver += (
                    self.artikel_quantity *
                    self.city.sell_price[self.artikel_name])
                self.city.increment_supply(self.artikel_name, self.artikel_quantity)
                self.open = False

        def cancel_click():
            self.open = False
            self.artikel_quantity = 0

        def dragbar_click():
            self.dragging = True

        dragbar_r_img = pygame.Surface([self.background_pane.image.get_width() - 2, 9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(dragbar_r_img,
                         dragbar_r_img,
                         dragbar_click,
                         1,
                         1)

        cancel_button = Button(cancel_r_img,
                               cancel_h_img,
                               cancel_click,
                               6,
                               130)

        done_button = Button(done_r_img,
                             done_h_img,
                             done_click,
                             90,
                             130)

        quantity_up_button = Button(arrow_r_r_img,
                                    arrow_r_h_img,
                                    quantity_up_click,
                                    157,
                                    58)

        quantity_down_button = Button(arrow_l_r_img,
                                      arrow_l_h_img,
                                      quantity_down_click,
                                      3,
                                      58)

        max_button = Button(max_r_img,
                            max_h_img,
                            max_click,
                            137,
                            96)

        min_button = Button(min_r_img,
                            min_h_img,
                            min_click,
                            3,
                            96)

        self.buttons = [done_button,
                        cancel_button,
                        quantity_up_button,
                        quantity_down_button,
                        max_button,
                        min_button,
                        dragbar]

    def keydown_handler(self, event, key):
        if key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
            self.step = 10
        elif key == pygame.K_LCTRL or key == pygame.K_RCTRL:
            self.step = 100

    def keyup_handler(self, event, key):
        if key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
            self.step = 1
        elif key == pygame.K_LCTRL or key == pygame.K_RCTRL:
            self.step = 1

    def update_display_cache(self):
        self.display_cache["artikel quantity"] = str(self.artikel_quantity)
        cost = self.artikel_quantity * self.transaction_modifiers[self.transaction_type]
        self.display_cache["transaction cost"] = str(cost)

    def render_decals(self, pos):
        small_font = pygame.font.SysFont("Calibri", 14, True, False)
        left_margin = (
            (self.background_pane.image.get_width() / 2) -
            (self.display_cache["artikel name"].get_width() / 2))
        self.cached_image.blit(self.display_cache["artikel name"], [left_margin, 13])
        self.cached_image.blit(small_font.render("0",
                                                 True,
                                                 (255, 255, 255)),
                               [6, 80])
        self.cached_image.blit(small_font.render(str(self.display_cache["artikel max"]),
                                                 True,
                                                 (255, 255, 255)),
                               [150, 80])

        quantity_stamp = small_font.render(self.display_cache["artikel quantity"],
                                           True,
                                           (255, 255, 255))
        cost_string = self.display_cache["transaction cost"]
        cost_stamp = small_font.render(
            "₴ {0} ".format(str(cost_string)),
            True,
            self.transaction_colors[self.transaction_type])
        quantity_margin = (
            (self.background_pane.image.get_width() / 2) -
            (quantity_stamp.get_width() / 2))
        cost_margin = (
            (self.background_pane.image.get_width() / 2) -
            (cost_stamp.get_width() / 2))
        self.cached_image.blit(quantity_stamp, [quantity_margin, 80])
        self.cached_image.blit(cost_stamp, [cost_margin, 60])


class MiniMap(Menu):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        map_image = game_state.active_map.biome_map_preview
        self.background_pane.image = art.mini_map_preview
        self.background_pane.image.blit(pygame.transform.rotate(map_image, -45),
                                        [2, 2])
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = game_state.screen_width - 200
        self.background_pane.rect.y = 0

        def recenter_click():
            x1, y1 = util.get_screen_coords(
                self.game_state.player.ship.column,
                self.game_state.player.ship.row)
            self.game_state.active_map.x_shift = (
                -x1 - 40 - self.game_state.background_width / 2 +
                self.game_state.screen_width / 2)
            self.game_state.active_map.y_shift = (
                -y1 - 40 + self.game_state.screen_height / 2)

        recenter = Button(
            recenter_r_img,
            recenter_h_img,
            recenter_click,
            0,
            self.background_pane.image.get_height() - 56)

        self.buttons = [recenter]

    def mouse_click_handler(self, event, pos):
        mouse_pos = (pos[0] - self.background_pane.rect.x + 2,
                     pos[1] - self.background_pane.rect.y + 2)
        for button in self.buttons:
            if util.check_if_inside(button.sprite.rect.x,
                                    button.sprite.rect.right,
                                    button.sprite.rect.y,
                                    button.sprite.rect.bottom,
                                    mouse_pos):
                button.click()
                return

        x1 = self.game_state.background_width
        y1 = self.game_state.background_height
        x2 = x1 / (self.background_pane.image.get_width() - 2)
        y2 = y1 / (self.background_pane.image.get_height() - 2)
        x3 = mouse_pos[0] * x2 - self.game_state.screen_width / 2
        y3 = mouse_pos[1] * y2 - self.game_state.screen_height / 2
        self.game_state.active_map.x_shift = -x3
        self.game_state.active_map.y_shift = -y3

    def render_decals(self, pos):
        def get_visible_tile_square(
                x_shift,
                y_shift,
                background_x_middle,
                width,
                height):
            xw = math.floor(width / 40)
            yh = math.floor(height / 15)
            x = width - 198
            y = 2
            x2 = x - (x_shift / 40)
            y2 = y - (y_shift / 15)
            tile_square = pygame.Rect(x2, y2, xw, yh)
            # tile_square = tile_square.move(0, 0)
            return tile_square, x2, y2

        (background_left,
         background_top,
         background_right,
         background_bottom,
         background_x_middle) = self.game_state.display_parameters
        visible_tile_square, x, y = get_visible_tile_square(
            background_left,
            background_top,
            background_x_middle,
            self.game_state.screen.get_width(),
            self.game_state.screen.get_height())
        visible_tile_square.x -= self.background_pane.rect.x
        visible_tile_square.y -= self.background_pane.rect.y
        pygame.draw.rect(self.cached_image, util.colors.red, visible_tile_square, 1)

    def render_onscreen_cache(self, pos):
        self.background_pane.rect.x = self.game_state.screen_width - 200
        self.cached_image = pygame.Surface([self.background_pane.image.get_width(),
                                            self.background_pane.image.get_height()])
        self.render_buttons(pos)
        self.cached_image.blit(self.background_pane.image, [0, 0])
        for button in self.buttons:
            self.cached_image.blit(button.sprite.image,
                                   [button.sprite.rect.x, button.sprite.rect.y])
        self.render_decals(pos)


class CalendarMenu(Menu):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = art.calendar_menu
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = 0
        self.background_pane.rect.y = 0

        def pause_toggle_click():
            self.game_state.paused = not self.game_state.paused
            print(self.game_state.paused)

        def faster_click():
            if self.game_state.game_speed == 240:
                self.game_state.game_speed = 120
            elif self.game_state.game_speed == 120:
                self.game_state.game_speed = 90
            elif self.game_state.game_speed == 90:
                self.game_state.game_speed = 60
            elif self.game_state.game_speed == 60:
                self.game_state.game_speed = 30
            print(self.game_state.game_speed)

        def slower_click():
            if self.game_state.game_speed == 30:
                self.game_state.game_speed = 60
            elif self.game_state.game_speed == 60:
                self.game_state.game_speed = 90
            elif self.game_state.game_speed == 90:
                self.game_state.game_speed = 120
            elif self.game_state.game_speed == 120:
                self.game_state.game_speed = 240
            print(self.game_state.game_speed)

        pause_toggle = Button(
            pause_toggle_r_img,
            pause_toggle_h_img,
            pause_toggle_click,
            26,
            2)

        faster = Button(
            faster_r_img,
            faster_h_img,
            faster_click,
            49,
            2)
        slower = Button(
            slower_r_img,
            slower_h_img,
            slower_click,
            3,
            2)

        self.buttons = [pause_toggle,
                        faster,
                        slower]

    def render_decals(self, pos):
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        date_string = self.game_state.calendar.get_date_string()
        date_stamp = header_font.render(date_string, True, util.colors.white)
        self.cached_image.blit(date_stamp, [80, 4])
