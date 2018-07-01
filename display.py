import pygame
import math
import utilities
import state
import art


tiny_font = pygame.font.SysFont('Calibri', 11, True, False)
small_font = pygame.font.SysFont('Calibri', 14, True, False)


def get_visible_tile_square(x_shift, y_shift, background_x_middle, width, height):
    xw = math.floor(width / 40)
    yh = math.floor(height / 15)
    x = width - 198
    y = 2
    x2 = x - (x_shift / 40)
    y2 = y - (y_shift / 15)
    tile_square = pygame.Rect(x2, y2, xw, yh)
    tile_square = tile_square.move(0, 0)
    return tile_square, x2, y2


def print_stats(game_state, selected_construct):
    pass


def update_display(game_state, selected_tile, background_left, background_top, background_right, background_bottom, background_x_middle, mouse_pos):
    active_map = game_state.active_map
    screen = game_state.screen
    game_state.screen.fill(utilities.colors.background_blue)
    map_image = active_map.biome_map_preview

    visible_tile_square, x, y = get_visible_tile_square(background_left,
                                                        background_top,
                                                        background_x_middle,
                                                        screen.get_width(),
                                                        screen.get_height())
    # game_state.screen.blit(active_map.tile_display_layer.image, [background_left,
                                                                 # background_top])

    if selected_tile:
        selected_coords = utilities.get_screen_coords(selected_tile.column,
                                                      selected_tile.row)

    screen.blit(active_map.terrain_display_layer.image, [background_left,
                                                         background_top])
    screen.blit(active_map.resource_display_layer.image, [background_left,
                                                          background_top])
    screen.blit(active_map.building_display_layer.image, [background_left,
                                                          background_top])
    player_coordinates = utilities.get_screen_coords(game_state.player.column, game_state.player.row)
    screen.blit(game_state.player.image, [player_coordinates[0] + background_left, player_coordinates[1] + background_top])
    print(player_coordinates[0] + background_left, player_coordinates[1] + background_top)
    screen.blit(art.mini_map_preview, [screen.get_width() - 200, 0])
    screen.blit(pygame.transform.rotate(map_image, -45), [screen.get_width() - 198, 2])
    pygame.draw.rect(screen, utilities.colors.red, visible_tile_square, 1)

    pygame.display.flip()

