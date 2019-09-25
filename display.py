import pygame
import utilities as util
import art


tiny_font = pygame.font.SysFont('Calibri', 11, True, False)
small_font = pygame.font.SysFont('Calibri', 14, True, False)


def print_stats(game_state, selected_construct):
    pass


def update_display(game_state, selected_tile, display_parameters, mouse_pos, map_xy):
    (background_left,
     background_top,
     background_right,
     background_bottom,
     background_x_middle) = display_parameters
    active_map = game_state.active_map
    screen = game_state.screen
    game_state.screen.fill(util.colors.background_blue)
    tile_width = 40

    game_state.screen.blit(active_map.tile_display_layer.image, [background_left,
                                                                 background_top])

    if selected_tile:
        st_pixel_coordinates = util.get_screen_coords(map_xy[0], map_xy[1])
        st_screen_coordinates = (
            st_pixel_coordinates[0] + background_x_middle + (tile_width / 2) - 20,
            st_pixel_coordinates[1] + background_top)
        screen.blit(
            art.selected_tile_image,
            [st_screen_coordinates[0],
             st_screen_coordinates[1]])

    screen.blit(active_map.terrain_display_layer.image, [background_left,
                                                         background_top])
    screen.blit(active_map.resource_display_layer.image, [background_left,
                                                          background_top])
    screen.blit(active_map.building_display_layer.image, [background_left,
                                                          background_top])

    if game_state.player.ship.path and game_state.draw_routes:
        shifted_pts_list = []
        for point in game_state.player.ship.path_pts:
            shifted_pts_list.append(
                (point[0] + background_x_middle + (tile_width / 2),
                 point[1] + background_top + 7))  # half tile height
        pygame.draw.aalines(screen, util.colors.red, False, shifted_pts_list)

    # converts the player's x, y tile to pixel coordinates
    player_pixel_coordinates = util.get_screen_coords(game_state.player.ship.column,
                                                      game_state.player.ship.row)
    # offsets the true pixel coordinates by the current display shift
    player_screen_coordinates = (
        player_pixel_coordinates[0] + background_x_middle + (tile_width / 2),
        player_pixel_coordinates[1] + background_top)
    """20 and 25 are graphical offsets - x and y
    so that the player's ship image is centered on the tile"""
    screen.blit(game_state.player.ship.image, [player_screen_coordinates[0] - 20,
                                               player_screen_coordinates[1] - 25])
    for menu in reversed(game_state.active_menus):
        game_state.screen.blit(
            menu.cached_image,
            [menu.background_pane.rect.x,
             menu.background_pane.rect.y])

    pygame.display.flip()

