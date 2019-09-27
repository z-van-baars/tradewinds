import math
import utilities as util


def render_height_map(mgs, marker, viable_sites):
    active_map = mgs.active_map
    raw_maps = mgs.raw_maps
    width = mgs.width
    height = mgs.height
    print("drawing heightmap...")
    for y in range(height):
        for x in range(width):
            value = math.floor(active_map.elevation[y][x] * 255)
            marker.fill((value, value, value))
            raw_maps[0].blit(marker, [x, y])


def render_temp_map(mgs, marker, viable_sites):
    active_map = mgs.active_map
    raw_maps = mgs.raw_maps
    width = mgs.width
    height = mgs.height
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


def render_moisture_map(mgs, marker, viable_sites):
    active_map = mgs.active_map
    raw_maps = mgs.raw_maps
    width = mgs.width
    height = mgs.height

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


def render_biome_map(mgs, marker, viable_sites):
    active_map = mgs.active_map
    raw_maps = mgs.raw_maps
    width = mgs.width
    height = mgs.height
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


def render_city_score_map(mgs, marker, viable_sites):
    raw_maps = mgs.raw_maps
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


def render_trade_score_map(mgs, marker, viable_sites):
    raw_maps = mgs.raw_maps
    raw_maps[4].fill((3, 0, 87))
    print("rendering trade score map")
    max_score = 25
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


def render_water_flux_map(mgs, marker, viable_sites):
    active_map = mgs.active_map
    raw_maps = mgs.raw_maps
    width = mgs.width
    height = mgs.height
    print("rendering water flux")
    max_flux = 0
    for each_row in active_map.game_tile_rows:
        for each_tile in each_row:
            if each_tile.water_flux[2] > max_flux:
                max_flux = each_tile.water_flux[2]
    flux_gradient = {0: (32, 5, 132),
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


def render_nation_map(mgs, marker, viable_sites):
    active_map = mgs.active_map
    raw_maps = mgs.raw_maps
    width = mgs.width
    height = mgs.height
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
