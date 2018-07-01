import pygame
import utilities
import game_map
import state
import display
import mapgen
import random
import player

pygame.init()
pygame.display.set_mode([0, 0])


def do_nothing(game_state):
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


key_functions = {pygame.K_UP: up_key,
                 pygame.K_DOWN: down_key,
                 pygame.K_LEFT: left_key,
                 pygame.K_RIGHT: right_key}


def input_processing(game_state, selected_tile, background_left, background_top, background_right, background_bottom, background_x_middle, mouse_pos):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
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
        mouse_pos = pygame.mouse.get_pos()
        map_xy = utilities.get_map_coords(mouse_pos,
                                          game_state.active_map.x_shift,
                                          game_state.active_map.y_shift,
                                          background_x_middle)

        selected_tile = None
        if 0 <= map_xy[0] <= active_map.width - 1 and 0 <= map_xy[1] <= active_map.height - 1:
            selected_tile = active_map.game_tile_rows[map_xy[1]][map_xy[0]]
        input_processing(game_state, selected_tile, background_left, background_top,
                         background_right, background_bottom, background_x_middle, mouse_pos)

        game_state.calendar.increment_date(game_state.game_speed)

        display.update_display(game_state, selected_tile, background_left, background_top,
                               background_right, background_bottom, background_x_middle, mouse_pos)

        game_state.clock.tick(60)
        game_state.time += 1


screen_width = 1600
screen_height = 1000

game_state = state.GameState(screen_width, screen_height)


game_state.active_map = game_map.Map((200, 200), (screen_width, screen_height))
mapgen.map_generation(game_state.active_map)
start_location = random.choice(game_state.active_map.cities)
# game_state.player = player.Player(start_location.column, start_location.row)
game_state.player = player.Player(100, 100)
print(start_location.column, start_location.row)
main(game_state)
