import pygame
import utilities as util
import game_map
import state
import display
import mapgen
import random
from player import Player
import ui
from typing import Dict
import ships

pygame.init()
pygame.display.set_mode([0, 0], pygame.RESIZABLE)


def do_nothing(game_state, mouse_pos=(0, 0), map_xy=(0, 0), *button_states):
    pass


def up_key(game_state):
    game_state.active_map.world_scroll(0,
                                       40,
                                       game_state.screen_width,
                                       game_state.screen_height)


def down_key(game_state):
    game_state.active_map.world_scroll(0,
                                       -40,
                                       game_state.screen_width,
                                       game_state.screen_height)


def left_key(game_state):
    game_state.active_map.world_scroll(40,
                                       0,
                                       game_state.screen_width,
                                       game_state.screen_height)


def right_key(game_state):
    game_state.active_map.world_scroll(-40,
                                       0,
                                       game_state.screen_width,
                                       game_state.screen_height)


def esc_key(game_state):
    new_options_menu = ui.OptionsMenu(game_state)
    game_state.clear_menutype([ui.OptionsMenu])
    game_state.active_menus.insert(0, new_options_menu)


def s_key(game_state):
    if any(menu_type == ui.ShipStatus for menu_type in game_state.active_menus):
        return
    new_ship_status_menu = ui.ShipStatus(game_state)
    game_state.clear_menutype([ui.ShipStatus])
    game_state.active_menus.insert(0, new_ship_status_menu)


def F1_key(game_state):
    if any(menu_type == ui.ConsoleWindow for menu_type in game_state.active_menus):
        return
    new_console_window = ui.ConsoleWindow(game_state)
    game_state.clear_menutype([ui.ConsoleWindow])
    game_state.active_menus.insert(0, new_console_window)


def left_click(game_state, mouse_pos, map_xy, button_states, event):
    if event.type == pygame.MOUSEBUTTONUP:
        for menu in game_state.active_menus:
            menu.event_handler(event, mouse_pos)
            return
    for menu in game_state.active_menus:
        interacted = menu.get_interaction(event, mouse_pos)
        if interacted:
            break
    if not interacted:
        c = game_state.active_map.game_tile_rows[map_xy[1]][map_xy[0]].city
        if c is None:
            return
        new_city_menu = ui.ViewCity(game_state, c)
        game_state.active_menus.insert(0, new_city_menu)
        menu = new_city_menu
    top_menu = menu
    game_state.active_menus.remove(menu)
    game_state.active_menus = [top_menu] + game_state.active_menus
    game_state.active_menus[0].event_handler(event, mouse_pos)


def scrollwheel_click(game_state, mouse_pos, map_xy, button_states, event):
    pass


def right_click(game_state, mouse_pos, map_xy, button_states, event):
    tile = game_state.active_map.game_tile_rows[map_xy[1]][map_xy[0]]
    game_state.clear_menutype([ui.ContextMenu,
                               ui.CityMenu,
                               ui.MarketMenu,
                               ui.TileInfoPane,
                               ui.ImpassablePopup])
    new_context_menu = ui.ContextMenu(game_state, mouse_pos, tile)
    game_state.active_menus = [new_context_menu] + game_state.active_menus


key_functions = {pygame.K_F1: F1_key,
                 pygame.K_UP: up_key,
                 pygame.K_DOWN: down_key,
                 pygame.K_LEFT: left_key,
                 pygame.K_RIGHT: right_key,
                 pygame.K_ESCAPE: esc_key,
                 pygame.K_s: s_key}

mouseclick_functions = {(1, 0, 0): left_click,
                        (0, 1, 0): scrollwheel_click,
                        (0, 0, 1): right_click}


def input_processing(game_state, selected_tile, display_parameters, mouse_pos, map_xy):
    (background_left,
     background_top,
     background_right,
     background_bottom,
     background_x_middle) = display_parameters
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button_1, button_2, button_3 = pygame.mouse.get_pressed()
            button_states = (button_1, button_2, button_3)
            mouseclick_functions.get(button_states,
                                     do_nothing)(game_state,
                                                 mouse_pos,
                                                 map_xy,
                                                 button_states,
                                                 event)
        elif event.type == pygame.MOUSEBUTTONUP:
            button_1, button_2, button_3 = pygame.mouse.get_pressed()
            button_states = (button_1, button_2, button_3)
            left_click(game_state, mouse_pos, map_xy, button_states, event)
        elif event.type == pygame.KEYDOWN:
            if len(game_state.active_menus) > 2:
                game_state.active_menus[0].event_handler(event, mouse_pos)
                return
            key_functions.get(event.key, do_nothing)(game_state)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                game_state.control = False
        elif event.type == pygame.VIDEORESIZE:
            game_state.screen = pygame.display.set_mode((event.w, event.h),
                                                        pygame.RESIZABLE)
            game_state.screen_width = event.w
            game_state.screen_height = event.h


def new_game(game_state, map_dimensions):
    game_state.active_map = game_map.Map(map_dimensions, (screen_width, screen_height))
    mapgen.map_generation(game_state, game_state.active_map)
    game_state.active_map.plr = Player(game_state, game_state.active_map)
    game_state.active_map.agents.add(game_state.active_map.plr)
    game_state.active_map.plr.ship = ships.Galleon(game_state.active_map, 0, 0)
    game_state.active_map.plr.silver = 100
    game_state.active_map.plr.ship.cargo['wool'] = 10

    """Randomize Start Location"""
    start_location = random.choice(game_state.active_map.cities)
    game_state.active_map.plr.column = start_location.column
    game_state.active_map.plr.row = start_location.row
    game_state.active_map.plr.ship.column = start_location.column
    game_state.active_map.plr.ship.row = start_location.row
    game_state.active_map.plr.column = start_location.column
    game_state.active_map.plr.row = start_location.row

    """Center Camera on Start"""
    x1, y1 = util.get_screen_coords(
        game_state.active_map.plr.ship.column,
        game_state.active_map.plr.ship.row)
    game_state.active_map.x_shift = (
        -x1 - 40 - game_state.background_width / 2 + game_state.screen_width / 2)
    game_state.active_map.y_shift = -y1 - 40 + game_state.screen_height / 2
    mini_map = ui.MiniMap(game_state)
    calendar_menu = ui.CalendarMenu(game_state)
    game_state.active_menus.append(mini_map)
    game_state.active_menus.append(calendar_menu)


def game_tick(game_state):
    # game_state.active_map.player.tick()
    for each_agent in game_state.active_map.agents:
        each_agent.tick()
    for each_city in game_state.active_map.cities:
        pass
        # each_city.turn_loop()


def main(game_state):
    active_map = game_state.active_map
    done = False

    while not done:
        mouse_pos = pygame.mouse.get_pos()
        map_xy = util.get_map_coords(mouse_pos,
                                     game_state.active_map.x_shift,
                                     game_state.active_map.y_shift,
                                     game_state.background_x_middle)
        selected_tile = None
        if util.check_if_inside(0,
                                active_map.width - 1,
                                0,
                                active_map.height - 1,
                                map_xy):
            selected_tile = active_map.game_tile_rows[map_xy[1]][map_xy[0]]
        input_processing(game_state,
                         selected_tile,
                         game_state.display_parameters,
                         mouse_pos,
                         map_xy)

        if game_state.time % game_state.game_speed == 0:
            game_state.calendar.increment_date()
            game_tick(game_state)

        display.update_display(game_state,
                               selected_tile,
                               game_state.display_parameters,
                               mouse_pos,
                               map_xy)
        menu_cache = []
        for menu in game_state.active_menus:
            menu_cache.append(menu)
            menu.drag(mouse_pos)
            menu.render_onscreen_cache(mouse_pos)
        game_state.active_menus = []
        for menu in menu_cache:
            if menu.open:
                game_state.active_menus.append(menu)

        # game_state.clock.tick(60)
        if not game_state.paused:
            game_state.time += 1


screen_width = 1200
screen_height = 800

game_state = state.GameState(screen_width, screen_height)

main_menu = ui.MainMenu(game_state)
game_state.active_menus.append(main_menu)
while main_menu.open:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button_1, button_2, button_3 = pygame.mouse.get_pressed()
            button_states = (button_1, button_2, button_3)
            if button_states[0]:
                game_state.active_menus[0].event_handler(event, mouse_pos)
        elif event.type == pygame.VIDEORESIZE:
            game_state.screen = pygame.display.set_mode((event.w, event.h),
                                                        pygame.RESIZABLE)
            game_state.screen_width = event.w
            main_menu.background_pane.rect.x = (
                game_state.screen.get_width() / 2 -
                main_menu.background_pane.image.get_width() / 2)
            game_state.screen_height = event.h

    game_state.screen.fill(util.colors.black)
    for menu in reversed(game_state.active_menus):
        game_state.screen.blit(
            menu.cached_image,
            [menu.background_pane.rect.x,
             menu.background_pane.rect.y])
    pygame.display.flip()
    game_state.clock.tick(60)

    menu_cache = []
    for menu in game_state.active_menus:
        menu_cache.append(menu)
        menu.render_onscreen_cache(mouse_pos)
    game_state.active_menus = []
    for menu in menu_cache:
        if menu.open:
            game_state.active_menus.append(menu)

if game_state.active_map is None:
    new_game(game_state, (200, 200))


main(game_state)


x = {"foo": 3}  # type: Dict[str, int]


def foobaz(zar: Dict[str, int]) -> int:
    return zar["foo"]


foobaz(x)
