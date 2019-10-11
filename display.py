import pygame
import utilities as util
import art


tiny_font = pygame.font.SysFont('Calibri', 11, True, False)
small_font = pygame.font.SysFont('Calibri', 14, True, False)
horizontal_ship_offset = 25
vertical_ship_offset = 35


def update_display(game_state, selected_tile, display_parameters, mouse_pos, map_xy):
    tile_width = 40
    (background_left,
     background_top,
     background_right,
     background_bottom,
     background_x_middle) = display_parameters
    active_map = game_state.active_map
    plr = active_map.plr
    screen = game_state.screen
    game_state.screen.fill(util.colors.background_blue)

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

    if plr.path is not None and game_state.draw_routes:
        shifted_pts_list = []
        pixel_xy = util.get_screen_coords(plr.column, plr.row)
        shifted_pts_list.append(
            (pixel_xy[0] + background_x_middle + (tile_width / 2),
             pixel_xy[1] + background_top + 7))
        for point in plr.path.steps:
            pixel_xy = util.get_screen_coords(point.column, point.row)
            shifted_pts_list.append(
                (pixel_xy[0] + background_x_middle + (tile_width / 2),
                 pixel_xy[1] + background_top + 7))  # half tile height
        pygame.draw.aalines(screen, util.colors.red, False, shifted_pts_list)

    for agent in game_state.active_map.agents:
        if agent.ship:
            # converts the agent's x, y tile to pixel coordinates
            agent_pixel_xy = util.get_screen_coords(
                agent.ship.column,
                agent.ship.row)
            # offsets the true pixel coordinates by the current display shift
            screen_xy = (
                agent_pixel_xy[0] + background_x_middle + (tile_width / 2),
                agent_pixel_xy[1] + background_top)
            """25 and 35 are graphical offsets - x and y
            so that the agent's ship image is centered on the tile
            defined at the top of this module"""
            game_state.screen.blit(
                agent.ship.image,
                [screen_xy[0] - horizontal_ship_offset,
                 screen_xy[1] - vertical_ship_offset])
    if game_state.draw_borders:
        screen.blit(active_map.nation_border_display_layer.image, [background_left,
                                                                   background_top])
    if game_state.draw_move_timer:
        timer_color = util.colors.light_green
        move_timer_stamp = tiny_font.render(str(plr.move_timer), True, timer_color)
        plr_pixel_xy = util.get_screen_coords(
            plr.ship.column,
            plr.ship.row)
        screen_xy = (
            plr_pixel_xy[0] + background_x_middle + (tile_width / 2),
            plr_pixel_xy[1] + background_top)
        screen.blit(move_timer_stamp, [screen_xy[0] + 15, screen_xy[1]])
    for menu in reversed(game_state.active_menus):
        game_state.screen.blit(
            menu.cached_image,
            [menu.background_pane.rect.x,
             menu.background_pane.rect.y])

    pygame.display.flip()

