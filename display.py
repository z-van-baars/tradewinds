import pygame
import math
import utilities
import state


tiny_font = pygame.font.SysFont('Calibri', 11, True, False)
small_font = pygame.font.SysFont('Calibri', 14, True, False)


def print_stats(game_state, selected_construct):
    pass


def update_display(game_state, selected_tile, background_left, background_top, background_right, background_bottom, background_x_middle, mouse_pos):
    active_map = game_state.active_map
    game_state.screen.fill(utilities.colors.background_blue)
    game_state.screen.blit(active_map.tile_display_layer.image, [background_left,
                                                                 background_top])

    if selected_tile:
        selected_coords = utilities.get_screen_coords(selected_tile.column,
                                                      selected_tile.row)

    game_state.screen.blit(active_map.terrain_display_layer.image, [background_left,
                                                                    background_top])
    # game_state.screen.blit(active_map.building_display_layer.image, [background_left,
                                                                     # background_top])

    pygame.display.flip()
