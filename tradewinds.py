import pygame
import utilities as util
import game_map
import state
import display
import mapgen
import random
import player
import ui

pygame.init()
pygame.display.set_mode([0, 0])


def do_nothing(game_state, mouse_pos=(0, 0), map_xy=(0, 0), button_states=None):
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


def left_click(game_state, mouse_pos, map_xy, button_states):
    pass


def scrollwheel_click(game_state, mouse_pos, map_xy, button_states):
    pass


def right_click(game_state, mouse_pos, map_xy, button_states):
    tile = game_state.active_map.game_tile_rows[map_xy[1]][map_xy[0]]
    new_context_menu = ui.ContextMenu(game_state, mouse_pos, tile)
    new_context_menu.menu_onscreen()


key_functions = {pygame.K_UP: up_key,
                 pygame.K_DOWN: down_key,
                 pygame.K_LEFT: left_key,
                 pygame.K_RIGHT: right_key}

mouseclick_functions = {(1, 0, 0): left_click,
                        (0, 1, 0): scrollwheel_click,
                        (0, 0, 1): right_click}


def input_processing(game_state, selected_tile, display_parameters, mouse_pos, map_xy):
    background_left, background_top, background_right, background_bottom, background_x_middle = display_parameters
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button_1, button_2, button_3 = pygame.mouse.get_pressed()
            button_states = (button_1, button_2, button_3)
            mouseclick_functions.get(button_states, do_nothing)(game_state, mouse_pos, map_xy, button_states)
        elif event.type == pygame.KEYDOWN:
            key_functions.get(event.key, do_nothing)(game_state)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                game_state.control = False


def main(game_state):
    active_map = game_state.active_map

    done = False

    background_width = game_state.active_map.tile_display_layer.image.get_width()
    background_height = game_state.active_map.tile_display_layer.image.get_height()
    active_map.x_shift = game_state.screen_width / 2 - background_width / 2
    active_map.y_shift = game_state.screen_height / 2 - (background_height / 2)
    game_state.year = 1000

    while not done:
        game_state.time += 1
        background_left = game_state.active_map.x_shift
        background_top = game_state.active_map.y_shift
        background_x_middle = 20 + (background_left + background_width / 2)
        background_bottom = (background_top + background_height)
        background_right = (background_left + background_width)
        display_parameters = (background_left, background_top, background_right, background_bottom, background_x_middle)
        mouse_pos = pygame.mouse.get_pos()
        map_xy = util.get_map_coords(mouse_pos,
                                     game_state.active_map.x_shift,
                                     game_state.active_map.y_shift,
                                     background_x_middle)
        selected_tile = None
        if util.check_if_inside(0, active_map.width - 1, 0, active_map.height - 1, map_xy):
            selected_tile = active_map.game_tile_rows[map_xy[1]][map_xy[0]]
        input_processing(game_state, selected_tile, display_parameters, mouse_pos, map_xy)

        game_state.calendar.increment_date(game_state.game_speed)

        display.update_display(game_state, selected_tile, display_parameters, mouse_pos, map_xy)

        game_state.clock.tick(60)
        game_state.time += 1


screen_width = 1600
screen_height = 1000

game_state = state.GameState(screen_width, screen_height)


game_state.active_map = game_map.Map((200, 200), (screen_width, screen_height))
mapgen.map_generation(game_state.active_map)
start_location = random.choice(game_state.active_map.cities)
# game_state.player = player.Player(start_location.column, start_location.row)
game_state.player = player.Player(0, 5)
game_state.player.silver = 100
game_state.player.ship.cargo['wool'] = 10
print(start_location.column, start_location.row)
main(game_state)
