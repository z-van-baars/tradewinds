import math
import utilities as util
import sound
import pygame


def display_update(screen, raw_maps, display_data, clock):
    scaled_maps = scale_maps(raw_maps, display_data)
    render_rotated_maps(screen, scaled_maps, display_data)
    render_map_labels(screen, scaled_maps, display_data)


def input_loop(game_state,
               message="Press Enter to Continue",
               wait_message="Please Wait..."):
    message_font = pygame.font.SysFont('Calibri', 14, True, False)
    enter_message = message_font.render(message,
                                        True,
                                        util.colors.white)

    enter_key = False
    while not enter_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                sound.click.play()
                enter_key = True
                enter_message = message_font.render(wait_message,
                                                    True,
                                                    util.colors.white)
            elif event.type == pygame.VIDEORESIZE:
                game_state.screen = pygame.display.set_mode((event.w, event.h),
                                                            pygame.RESIZABLE)
                game_state.screen_width = event.w
                game_state.screen_height = event.h

        game_state.screen.fill(util.colors.black)
        display_update(game_state.screen,
                       game_state.active_map.raw_maps,
                       game_state.active_map.display_data,
                       game_state.clock)

        game_state.screen.blit(enter_message,
                               [10, game_state.screen_height - 24])
        pygame.display.flip()


def render_raw_maps(active_map, exclusive=None, viable_sites=None):

    tile_marker = pygame.Surface([1, 1])
    tile_marker.fill((0, 0, 0))
    render_funcs = {"height": render_height_map,
                    "moisture": render_moisture_map,
                    "temp": render_temp_map,
                    "water flux": render_water_flux_map,
                    "biome": render_biome_map,
                    "city score": render_city_score_map,
                    "trade score": render_trade_score_map,
                    "nation": render_nation_map}

    if exclusive is not None:
        for each in exclusive:
            render_funcs[each](active_map, tile_marker, viable_sites)
        return
    for map_type, render_func in render_funcs.items():
        render_func(active_map, tile_marker, viable_sites)


def render_height_map(active_map, marker, viable_sites):
    raw_maps = active_map.raw_maps
    width = active_map.width
    height = active_map.height
    print("drawing heightmap...")
    for y in range(height):
        for x in range(width):
            value = math.floor(active_map.elevation[y][x] * 255)
            marker.fill((value, value, value))
            raw_maps[0].blit(marker, [x, y])


def render_temp_map(active_map, marker, viable_sites):
    raw_maps = active_map.raw_maps
    width = active_map.width
    height = active_map.height
    print("drawing temperature map...")
    temp_gradient = {0: (0, 53, 191),
                     1: (0, 135, 195),
                     2: (0, 199, 177),
                     3: (0, 203, 95),
                     4: (0, 207, 10),
                     5: (77, 212, 0),
                     6: (169, 216, 0),
                     7: (220, 176, 0),
                     8: (224, 85, 0),
                     9: (229, 0, 7)}
    for y in range(height):
        for x in range(width):
            value = math.floor(max(0, (active_map.temperature[y][x] - 1)) * 0.1)
            marker.fill(temp_gradient[value])
            raw_maps[1].blit(marker, [x, y])


def render_moisture_map(active_map, marker, viable_sites):
    raw_maps = active_map.raw_maps
    width = active_map.width
    height = active_map.height

    print("drawing moisture map...")
    moisture_gradient = {0: (229, 131, 0),
                         1: (203, 124, 21),
                         2: (178, 118, 42),
                         3: (152, 111, 63),
                         4: (127, 105, 84),
                         5: (101, 98, 106),
                         6: (76, 92, 127),
                         7: (50, 85, 148),
                         8: (25, 79, 169),
                         9: (0, 73, 255)}
    for y in range(height):
        for x in range(width):
            value = math.floor(active_map.moisture[y][x])
            value = min(9, round((value / 100) * 10))
            marker.fill(moisture_gradient[value])
            raw_maps[2].blit(marker, [x, y])


def render_biome_map(active_map, marker, viable_sites):
    raw_maps = active_map.raw_maps
    width = active_map.width
    height = active_map.height
    print("drawing biome map...")
    for y in range(height):
        for x in range(width):
            biome = active_map.game_tile_rows[y][x].biome
            marker.fill(util.colors.biome_colors[biome])
            raw_maps[3].blit(marker, [x, y])

    marker.fill(util.colors.purple)
    for each in active_map.cities:
        # zoc_tiles = utilities.get_nearby_tiles(active_map, [each.column, each.row], 8)
        # for tile in zoc_tiles:
            # biome_map_image.blit(marker, [tile.column, tile.row])
        raw_maps[3].blit(marker, [each.column, each.row])
    marker.fill(util.colors.red)
    for row in active_map.game_tile_rows:
        for tile in row:
            if tile.resource:
                raw_maps[3].blit(marker, [tile.column, tile.row])


def render_city_score_map(active_map, marker, viable_sites):
    if viable_sites is None:
        return
    raw_maps = active_map.raw_maps
    raw_maps[5].fill((3, 0, 87))
    print("rendering city score map")
    max_score = 500
    score_gradient = {0: (3, 0, 87),
                      10: (59, 211, 13),
                      9: (78, 91, 13),
                      8: (97, 171, 13),
                      7: (116, 151, 13),
                      6: (135, 132, 13),
                      5: (154, 112, 13),
                      4: (173, 92, 13),
                      3: (192, 72, 13),
                      2: (211, 52, 13),
                      1: (231, 33, 13)}
    largest = 0

    for site in viable_sites:
        normalized_value = min(10, round((site.city_score / max_score) * 10))
        if site.city_score > largest:
            largest = site.city_score
        marker.fill(score_gradient[normalized_value])
        raw_maps[5].blit(marker, [site.tile.column, site.tile.row])


def render_trade_score_map(active_map, marker, viable_sites):
    if viable_sites is None:
        return
    raw_maps = active_map.raw_maps
    raw_maps[4].fill((3, 0, 87))
    print("rendering trade score map")
    max_score = 45
    score_gradient = {0: (3, 0, 87),
                      10: (59, 211, 13),
                      9: (78, 91, 13),
                      8: (97, 171, 13),
                      7: (116, 151, 13),
                      6: (135, 132, 13),
                      5: (154, 112, 13),
                      4: (173, 92, 13),
                      3: (192, 72, 13),
                      2: (211, 52, 13),
                      1: (231, 33, 13)}
    largest = 0
    for site in viable_sites:
        normalized_value = min(10, round((site.trade_score / max_score) * 10))
        if site.trade_score > largest:
            largest = site.trade_score
        marker.fill(score_gradient[normalized_value])
        raw_maps[4].blit(marker, [site.tile.column, site.tile.row])


def render_water_flux_map(active_map, marker, viable_sites):
    raw_maps = active_map.raw_maps
    width = active_map.width
    height = active_map.height
    print("rendering water flux")
    max_flux = 0
    for each_row in active_map.game_tile_rows:
        for each_tile in each_row:
            if each_tile.water_flux[2] > max_flux:
                max_flux = each_tile.water_flux[2]
    flux_gradient = {0: (32, 5, 102),
                     1: (69, 43, 158),
                     2: (85, 60, 154),
                     3: (101, 78, 149),
                     4: (118, 96, 145),
                     5: (135, 114, 141),
                     6: (151, 132, 137),
                     7: (167, 149, 133),
                     8: (200, 185, 125),
                     9: (234, 220, 116),
                     10: (250, 238, 112)}
    max_flux = active_map.mgp.river_cutoff * 1.25
    for y in range(height):
        for x in range(width):
            flux = active_map.game_tile_rows[y][x].water_flux[2]
            value = min(10, round((flux / max_flux) * 10))
            if active_map.game_tile_rows[y][x].biome in ("ocean",
                                                         "lake",
                                                         "shallows",
                                                         "sea"):
                value = 0
            marker.fill(flux_gradient[value])
            raw_maps[6].blit(marker, [x, y])
    print("Max Water Flux: {0}".format(max_flux))


def render_nation_map(active_map, marker, viable_sites):
    raw_maps = active_map.raw_maps
    width = active_map.width
    height = active_map.height
    print("drawing nation territory map...")
    for y in range(height):
        for x in range(width):
            n = active_map.nation_control[y][x]
            if not n:
                biome = active_map.game_tile_rows[y][x].biome
                if any([biome == "ocean",
                        biome == "sea",
                        biome == "shallows",
                        biome == "lake",
                        biome == "river"]):
                    marker.fill((27, 24, 81))
                else:
                    marker.fill((110, 110, 110))
            else:
                marker.fill(n.color)
            raw_maps[7].blit(marker, [x, y])
    marker.fill((255, 255, 255))
    for each in active_map.cities:
        # zoc_tiles = utilities.get_nearby_tiles(active_map, [each.column, each.row], 8)
        # for tile in zoc_tiles:
            # biome_map_image.blit(marker, [tile.column, tile.row])
        raw_maps[7].blit(marker, [each.column, each.row])


def prepare_map_surfaces(display_data):
    # prepares blank, properly sized, destination map surfaces
    display_width, display_height, display_scale = (display_data[0],
                                                    display_data[1],
                                                    display_data[2])
    if display_scale:
        display_width = 264
        display_height = 264

    map_surfaces = [pygame.Surface([display_width, display_height])
                    for i in range(8)]
    blank_maps = []
    for each in map_surfaces:
        each.fill((110, 110, 110))
        each.set_colorkey(util.colors.key)
        each = each.convert_alpha()
        blank_maps.append(each)
    return blank_maps


def scale_maps(raw_maps, display_data):
    # resizes raw maps and returns a list of resized surfaces
    display_width, display_height, display_scale = display_data
    if display_scale:
        display_width = 264
        display_height = 264
    # generate blank destination surfaces that are properly sized
    scaled_maps = prepare_map_surfaces(display_data)

    for i, raw_map in enumerate(raw_maps):
        pygame.transform.smoothscale(
            raw_map,
            (display_width, display_height), scaled_maps[i])
    return scaled_maps


def render_rotated_maps(screen, scaled_maps, display_data):
    # prints rendered and prepped map surfaces to the screen after rotating
    rotation = -45  # rotation for map previews in degrees
    display_width, display_height, display_scale = display_data
    if display_scale:
        c = math.sqrt(264 ** 2 + 264 ** 2)
    else:
        # offset for left edge of map displays
        c = pygame.transform.rotate(scaled_maps[0], -45).get_width()
    display_offset = 5
    # heightmap
    screen.blit(pygame.transform.rotate(scaled_maps[0], rotation),
                [0, 0])
    # tempmap
    screen.blit(pygame.transform.rotate(scaled_maps[1], rotation),
                [c + display_offset, 0])
    # moisture map
    screen.blit(pygame.transform.rotate(scaled_maps[2], rotation),
                [0, c + display_offset])
    # biome map with cities marked
    screen.blit(pygame.transform.rotate(scaled_maps[3], rotation),
                [c + display_offset, c + display_offset])
    # trade connectivity score map
    screen.blit(pygame.transform.rotate(scaled_maps[4], rotation),
                [c * 2 + display_offset * 2, 0])
    # city score map
    screen.blit(pygame.transform.rotate(scaled_maps[5], rotation),
                [c * 2 + display_offset * 2, c + display_offset])
    # water flux map
    screen.blit(pygame.transform.rotate(scaled_maps[6], rotation),
                [c * 3 + display_offset * 3, 0])
    # Nation Map
    screen.blit(pygame.transform.rotate(scaled_maps[7], rotation),
                [c * 3 + display_offset * 3, c + display_offset])


def render_map_labels(screen, scaled_maps, display_data):
    display_width, display_height, display_scale = display_data
    if display_scale:
        c = math.sqrt(264 ** 2 + 264 ** 2)
    else:
        # offset for left edge of map displays
        c = pygame.transform.rotate(scaled_maps[0], -45).get_width()
    display_offset = 5
    label_font = pygame.font.SysFont("Minion Pro", 26, False, False)
    screen.blit(label_font.render("Elevation", True, util.colors.white),
                [0, c])
    screen.blit(label_font.render("Temperature", True, util.colors.white),
                [c + display_offset, c])
    screen.blit(label_font.render("Moisture", True, util.colors.white),
                [0, c + display_offset + c])
    screen.blit(label_font.render("Biomes", True, util.colors.white),
                [c + display_offset, c + display_offset + c])
    screen.blit(label_font.render("Trade Score", True, util.colors.white),
                [c * 2 + display_offset * 2, c])
    screen.blit(label_font.render("City Score", True, util.colors.white),
                [c * 2 + display_offset * 2, c * 2 + display_offset])
    screen.blit(label_font.render("Water Flux", True, util.colors.white),
                [c * 3 + display_offset * 3, c])
    screen.blit(label_font.render("Nation Borders", True, util.colors.white),
                [c * 3 + display_offset * 3, c * 2 + display_offset])
