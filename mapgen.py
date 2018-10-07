from opensimplex import OpenSimplex
import utilities as util
import math
import random
import queue
import numpy as np
from scipy.ndimage import label, generate_binary_structure
from game_tile import GameTile
from game_map import Map
import pygame
import city
import artikel
import time
import region
import sound

pygame.init()
pygame.display.set_mode([0, 0])


def generate_heightmap(active_map):
    print("generating heightmap...")
    gen = OpenSimplex(random.randrange(100000))

    def noise(nx, ny):
        # rescale from -1.0:+1/0 to 0.0:1.0
        return gen.noise2d(nx, ny) / 2.0 + 0.5

    elevation = []
    width = len(active_map.game_tile_rows[0])
    height = len(active_map.game_tile_rows)
    for y in range(height):
        row = []
        for x in range(width):
            row.append(0)
        elevation.append(row)

    for y in range(height):
        for x in range(width):
            # print(x, y)
            nx = x / width - 0.5
            ny = y / height - 0.5
            # d = 2 * max(abs(nx), abs(ny))  # Manhattan Distance from edges
            d = 2 * math.sqrt(nx * nx + ny * ny)  # Euclidian Distance from edges
            a = 0.04  # pushes all land up (higher value means more land but also chance of edge touching)
            b = 0.24  # pushes the edges farther down
            c = 10.00  # how quick the elevation falloff is toward the edges
            new = (1.00 * noise(5 * nx, 5 * ny) +
                   0.5 * noise(16 * nx, 16 * ny) +
                   0.25 * noise(32 * nx, 32 * ny) +
                   0.13 * noise(64 * nx, 64 * ny))
            new = new / (1 + 0.5 + 0.25 + 0.13)
            new = new + a - b * pow(d, c)
            elevation[y][x] += max(new, 0)

    active_map.elevation = elevation


def generate_tempmap(width, height):
    print("generating tempmap...")
    gen = OpenSimplex(random.randrange(100000))

    def noise(nx, ny):
        # rescale from -1.0:+1/0 to 0.0:1.0
        return gen.noise2d(nx, ny) / 2.0 + 0.5

    def get_temperature(equator_hotness, pole_coldness, noise_strength, noisiness):
        nx = x / width - 0.5
        ny = y / height - 0.5
        new = (1.0 * noise(noisiness * nx, noisiness * ny))
        new = new / (noise_strength)
        max_distance = math.sqrt(width * height)
        distance_modifier = (pole_distances[y][x] / max_distance)
        # distance_modifier = distance_modifier ** distance_modifier
        # distance_modifier = distance_modifier / 50
        # print("{0} / {1} : {2}%".format(distance_modifier, max_distance, math.floor(distance_modifier / max_distance * 100)))
        temp = 1.0 + distance_modifier * equator_hotness - distance_modifier * pole_coldness
        new_temperature = min(math.floor(max((temp + (temp * new) * noise_strength) * abs(1.0 - noise_strength), 0) * 100), 100)
        return new_temperature

    def set_pole_distances():
        number_of_points = math.floor(math.sqrt(math.sqrt(width * height)))
        slope = (width / number_of_points, height / number_of_points)
        xx = 0
        yy = height
        equator = [(xx, yy)]
        for e in range(number_of_points + 2):
            xx += slope[0]
            yy -= slope[1]
            equator.append((math.floor(xx), math.floor(yy)))

        pole_distances = []
        for y in range(height):
            pole_distances.append([])
            for x in range(width):
                # north_pole = utilities.distance(0, 0, x, y)
                # south_pole = utilities.distance(width, height, x, y)
                equatorial_distances = []
                for each in equator:
                    equatorial_distances.append(util.distance(each[0], each[1], x, y))
                # equatorial_distance = min(north_pole, south_pole)
                equatorial_distance = min(equatorial_distances)
                pole_distances[y].append(math.floor(equatorial_distance))
        return pole_distances

    pole_distances = set_pole_distances()
    temperature = []
    equator_hotness = 1.0
    pole_coldness = 2.5
    noise_strength = 0.2
    noisiness = 10
    for y in range(height):
        temperature.append([])
        for x in range(width):

            # print(new, new_temperature)
            new_temperature = get_temperature(equator_hotness, pole_coldness, noise_strength, noisiness)
            temperature[y].append(new_temperature)
    return temperature


def generate_moisture_map(width, height, elevation, water_cutoff):
    print("generating moisture map...")
    gen = OpenSimplex(random.randrange(100000))

    def noise(nx, ny):
        # rescale from -1.0:+1/0 to 0.0:1.0
        return gen.noise2d(nx, ny) / 2.0 + 0.5
    moisture = []
    for y in range(height):
        moisture.append([])
        for x in range(width):
            nx = x / width - 0.5
            ny = y / height - 0.5
            new = (1.1 * noise(5 * nx, 5 * ny))
            new = new / (1.1)
            if elevation[y][x] < water_cutoff:
                new_moisture = 100
            else:
                new_moisture = min(100, new * 100 - (new * 75) * (elevation[y][x] - water_cutoff * 1.5))
            moisture[y].append(math.floor(new_moisture))

    return moisture


def classify_masses(active_map):
    print('classifying landmasses...')
    water_array = np.ones((active_map.width, active_map.height))
    for row in active_map.game_tile_rows:
        for tile in row:
            if active_map.elevation[tile.row][tile.column] >= active_map.water_cutoff:
                water_array[tile.column, tile.row] = 0
    s = generate_binary_structure(2, 2)
    labeled_array, num_features = label(water_array, structure=s)

    # filter the labeled array into layers. `==` does the filtering
    layers = [(labeled_array == i) for i in range(1, num_features + 1)]

    sorted_water_bodies = sorted(((np.sum(subarray), subarray) for subarray in layers), key=lambda x: x[0], reverse=True)
    lake_constant = math.floor(((active_map.width * active_map.height) ** (1 / 4)) * 3)
    print("{0} lake constant".format(lake_constant))
    small_water_bodies = []
    for size, water_body in sorted_water_bodies:
        if size < lake_constant:
            small_water_bodies.append(water_body)
    all_tiles = []
    for row in active_map.game_tile_rows:
        for tile in row:
            all_tiles.append(tile)
    tiles_to_raise = []
    for water_body in small_water_bodies:
        for new_tile in all_tiles:
            if water_body[new_tile.column, new_tile.row] == 1:
                tiles_to_raise.append(new_tile)
    return tiles_to_raise


def adjust_landmass_height(active_map):
    tiles_to_raise = classify_masses(active_map)
    print('adjusting interior landmass elevation...')
    print('tiles to raise: {0}'.format(len(tiles_to_raise)))
    raising = True
    while raising:
        raising = False
        for each_tile in tiles_to_raise:
            active_map.elevation[each_tile.row][each_tile.column] = min(active_map.water_cutoff + 0.01,
                                                                        active_map.elevation[each_tile.row][each_tile.column] + 0.01)
            if active_map.elevation[each_tile.row][each_tile.column] < active_map.water_cutoff + 0.01:
                raising = True


def infill_basins(active_map):
    print("filling basins...")
    water_cutoff = 0.5

    # builds a stack of layer tuples to iterate through
    z_layers = queue.PriorityQueue()
    for y_row in active_map.game_tile_rows:
        for tile in y_row:
            elevation = active_map.elevation[tile.row][tile.column]
            if active_map.elevation[tile.row][tile.column] > water_cutoff:
                z_layers.put((-elevation, tile))  # inverting the highest elevation brings it to the top of the queue for the get() operator

    # works from the highest z(elevation) to the lowest, adding water flux to lower tiles cumulatively
    while not z_layers.empty():
        elevation, tile = z_layers.get()
        neighbors = util.get_adjacent_tiles(tile, active_map)

        # builds a list of neighbors who are at a lower Z level
        flowable_neighbors = []
        all_neighbors = []  # backup list in case we bottom out and need to fill in a lake
        for each_tile in neighbors:
            if active_map.elevation[each_tile.row][each_tile.column] < active_map.elevation[tile.row][tile.column]:
                flowable_neighbors.append((active_map.elevation[each_tile.row][each_tile.column], each_tile))
            all_neighbors.append((active_map.elevation[each_tile.row][each_tile.column], each_tile))

        # if no neighboring tile is lower, then cease to flow, turn this tile into a SHALLOWS tile / LAKE
        if len(flowable_neighbors) == 0:
            frontier = sorted(all_neighbors)
            last_addition = tile
            last_addition_elevation = active_map.elevation[tile.row][tile.column]
            tiles_to_raise = [tile]
            while frontier[0][0] >= last_addition_elevation:
                last_addition = frontier[0][1]
                del frontier[0]
                last_addition_elevation = active_map.elevation[last_addition.row][last_addition.column]
                tiles_to_raise.append(last_addition)
                new_neighbors = util.get_adjacent_tiles(last_addition, active_map)
                for neighbor in new_neighbors:
                    if (active_map.elevation[neighbor.row][neighbor.column], neighbor) not in frontier:
                        if neighbor not in tiles_to_raise:
                            frontier.append((active_map.elevation[neighbor.row][neighbor.column], neighbor))
                            frontier = sorted(frontier)
                for tile_to_raise in tiles_to_raise:
                    active_map.elevation[tile_to_raise.row][tile_to_raise.column] = last_addition_elevation


def generate_rivers(active_map, water_cutoff):
    print("running rivers...")
    river_cutoff = active_map.river_cutoff

    # builds a stack of layer tuples to iterate through
    moisture_layers = queue.PriorityQueue()
    for y_row in active_map.game_tile_rows:
        for tile in y_row:
            elevation = active_map.elevation[tile.row][tile.column]
            if active_map.elevation[tile.row][tile.column] > water_cutoff:
                moisture_layers.put((-elevation, tile))  # inverting the highest elevation brings it to the top of the queue for the get() operator

    # works from the highest z(elevation) to the lowest, adding water flux to lower tiles cumulatively
    while not moisture_layers.empty():
        elevation, tile = moisture_layers.get()
        neighbors = util.get_adjacent_tiles(tile, active_map)

        # builds a list of neighbors who are at a lower Z level
        flowable_neighbors = []
        all_neighbors = []  # backup list in case we bottom out and need to fill in a lake
        for each_tile in neighbors:
            if active_map.elevation[each_tile.row][each_tile.column] < active_map.elevation[tile.row][tile.column]:
                flowable_neighbors.append((active_map.elevation[each_tile.row][each_tile.column], each_tile))
            all_neighbors.append((active_map.elevation[each_tile.row][each_tile.column], each_tile))

        # if no neighboring tile is lower, then cease to flow, turn this tile into a SHALLOWS tile / LAKE
        if len(flowable_neighbors) == 0:
            water_in = tile.water_flux[0]
            water_out = water_in
            total_flux = water_in + water_out + active_map.moisture[tile.row][tile.column]
            tile.water_flux = (water_in, water_out, total_flux)
            if total_flux >= river_cutoff:
                tile.biome = "lake"
                frontier = sorted(all_neighbors)
                last_addition = tile
                last_addition_elevation = active_map.elevation[tile.row][tile.column]
                tiles_filled = [tile]
                while frontier[0][0] >= last_addition_elevation:
                    last_addition = frontier[0][1]
                    last_addition_elevation = frontier[0][0]
                    del frontier[0]
                    last_addition.biome = "lake"
                    tiles_filled.append(last_addition)
                    last_addition.water_flux = (max(water_in, last_addition.water_flux[0]),
                                                max(water_out, last_addition.water_flux[1]),
                                                max(total_flux, last_addition.water_flux[2]))
                    new_neighbors = util.get_adjacent_tiles(last_addition, active_map)
                    for neighbor in new_neighbors:
                        if (active_map.elevation[neighbor.row][neighbor.column], neighbor) not in frontier:
                            if neighbor not in tiles_filled:
                                frontier.append((active_map.elevation[neighbor.row][neighbor.column], neighbor))
                                frontier = sorted(frontier)
                # frontier[0][1].water_flux = (frontier[0][1].water_flux[0] + water_in, 0, frontier[0][1].water_flux[2] + total_flux)
                # frontier[0][1].water_source = (frontier[0][1].water_source[0] + [util.get_neighbor_position(frontier[0][1], last_addition)], 0)
                frontier[0][1].water_flux = (water_in, 0, 0)
                frontier[0][1].water_source = ([util.get_neighbor_position(frontier[0][1], last_addition)], 0)

        # if we have >1 lower tile, add our collected water flux to it's water flux in
        else:
            lowest_neighbor = sorted(flowable_neighbors)[0][1]

            water_in, water_out, total_flux = tile.water_flux

            water_out = water_in + active_map.moisture[tile.row][tile.column]  # add incoming water flux to local moisture and send it out
            total_flux = water_in + water_out
            tile.water_source = (tile.water_source[0], util.get_neighbor_position(tile, lowest_neighbor))
            lowest_neighbor.water_flux = (water_out + lowest_neighbor.water_flux[0], 0, 0)
            if total_flux > river_cutoff:
                lowest_neighbor.water_source = (lowest_neighbor.water_source[0] + [util.get_neighbor_position(lowest_neighbor, tile)], 0)

            tile.water_flux = (water_in, water_out, total_flux)


def generate_blank_grass_tiles(active_map):
    active_map.game_tile_rows = []
    for y_row in range(active_map.height):
        this_row = []
        for x_column in range(active_map.width):
            this_row.append(GameTile(x_column, y_row, "grass"))
        active_map.game_tile_rows.append(this_row)


def generate_blank_ocean_tiles(active_map):
    active_map.game_tile_rows = []
    for y_row in range(active_map.height):
        this_row = []
        for x_column in range(active_map.width):
            this_row.append(GameTile(x_column, y_row, "ocean"))
        active_map.game_tile_rows.append(this_row)


def get_biome_parameters():
    biome_temps = {}
    for t in range(101):
        if 0 <= t < 20:
            temp = "very cold"
        elif 20 <= t < 40:
            temp = "cold"
        elif 40 <= t < 60:
            temp = "cool"
        elif 60 <= t < 85:
            temp = "warm"
        elif 85 <= t:
            temp = "hot"
        biome_temps[t] = temp
    biome_moisture = {}
    for m in range(101):
        if 0 <= m < 10:
            moisture = "very dry"
        elif 30 <= m < 40:
            moisture = "dry"
        elif 40 <= m < 60:
            moisture = "wet"
        elif 60 <= m:
            moisture = "very wet"
        biome_moisture[m] = moisture

    return biome_temps, biome_moisture


def pick_biome(temperature, moisture):
    biomes = {"very cold": {"very dry": "tundra",
                            "dry": "snowy tundra",
                            "wet": "snowpack",
                            "very wet": "snowpack"},
              "cold": {"very dry": "tundra",
                       "dry": "tundra",
                       "wet": "taiga",
                       "very wet": "snowpack"},
              "cool": {"very dry": "shrubland",
                       "dry": "grassland",
                       "wet": "taiga",
                       "very wet": "forest"},
              "warm": {"very dry": "savannah",
                       "dry": "plains",
                       "wet": "grassland",
                       "very wet": "forest"},
              "hot": {"very dry": "desert",
                      "dry": "savannah",
                      "wet": "plains",
                      "very wet": "jungle"}}

    return(biomes[temperature][moisture])


def generate_biomes(active_map, water_cutoff):
    shallows_cutoff = 0.5
    sea_cutoff = 0.45
    ocean_cutoff = 0.4
    biome_temps, biome_moisture = get_biome_parameters()
    for y_row in active_map.game_tile_rows:
        for tile in y_row:
            biome = "ocean"
            if active_map.elevation[tile.row][tile.column] >= shallows_cutoff:
                temperature = active_map.temperature[tile.row][tile.column]
                moisture = active_map.moisture[tile.row][tile.column]
                biome = pick_biome(biome_temps[temperature], biome_moisture[moisture])
                if biome == "plains":
                    if active_map.moisture[tile.row][tile.column] >= 55:
                        biome = "wet plains"
            elif shallows_cutoff > active_map.elevation[tile.row][tile.column] >= sea_cutoff:
                biome = "shallows"
            elif sea_cutoff > active_map.elevation[tile.row][tile.column] >= ocean_cutoff:
                biome = "sea"

            tile.biome = biome


def generate_terrain(active_map):
    print("generating terrain...")
    low_hill_cutoff = 0.7
    hill_cutoff = 0.725
    low_mountain_cutoff = 0.75
    mountain_cutoff = 0.775
    for y_row in active_map.game_tile_rows:
        for tile in y_row:
            if hill_cutoff > active_map.elevation[tile.row][tile.column] >= low_hill_cutoff:
                tile.terrain = "low hill"
            elif low_mountain_cutoff > active_map.elevation[tile.row][tile.column] >= hill_cutoff:
                tile.terrain = "hill"
            elif mountain_cutoff > active_map.elevation[tile.row][tile.column] >= low_mountain_cutoff:
                tile.terrain = "low mountain"
            elif active_map.elevation[tile.row][tile.column] >= mountain_cutoff:
                tile.terrain = "mountain"
            else:
                tile.terrain = "vegetation"


def check_local_resources(active_map, tile):
    tiles_in_radius = util.get_nearby_tiles(active_map, [tile.row, tile.column], 5)
    for each_tile in tiles_in_radius:
        if tile.resource:
            return False
    return True


def pick_random_location(active_map):
    selected = False
    while not selected:
        tile_xy = util.get_random_coordinates(0, active_map.width - 1, 0, active_map.height - 1)
        if check_local_resources(active_map, active_map.game_tile_rows[tile_xy[1]][tile_xy[0]]):
            selected = True
    tile = active_map.game_tile_rows[tile_xy[1]][tile_xy[0]]
    return tile


def pick_from_available_resources(active_map, tile):
    possible_resources = artikel.possible_resources[tile.terrain][tile.biome]
    return(random.choice(possible_resources))


def place_resources(active_map, max_cluster_size):
    max_retries = 5
    number_of_clusters = math.floor(math.sqrt(active_map.width * active_map.height) / 4)
    print("placing resources...")
    print("number of clusters: {0}".format(number_of_clusters))
    for ii in range(number_of_clusters):
        cluster_size = random.randint(1, max_cluster_size)
        tile_chosen = False
        while not tile_chosen:
            tile = pick_random_location(active_map)
            resource_choice = pick_from_available_resources(active_map, tile)
            if resource_choice:
                tile_chosen = True
        active_map.game_tile_rows[tile.row][tile.column].resource = resource_choice

        nearby_tiles = util.get_nearby_tiles(active_map, [tile.row, tile.column], 5)
        for jj in range(cluster_size):
            try_count = 0
            clear_matching_tile = False
            while not clear_matching_tile:
                try_count += 1
                if try_count > max_retries:
                    break
                new_resource = random.choice(nearby_tiles)
                if new_resource.biome == tile.biome:
                    clear_matching_tile = True
                    nearby_tiles.remove(new_resource)
                    active_map.game_tile_rows[new_resource.row][new_resource.column].resource = resource_choice


def city_score_to_array(active_map, city_scores):
    # turns an input dict - city scores - into an output array - city score array
    city_score_array = []

    for y in range(active_map.height):
        new_row = []
        for x in range(active_map.width):
            new_row.append(0)
        city_score_array.append(new_row)
    for site, score in city_scores.items():
        active_map.city_score[site.row][site.column] = score
    return city_score_array


def render_raw_maps(active_map, width, height, raw_maps, exclusive=None, viable_sites=None):
    tile_marker = pygame.Surface([1, 1])
    tile_marker.fill((0, 0, 0))
    if not exclusive or exclusive == "height":
        print("drawing heightmap...")
        for y in range(height):
            for x in range(width):
                value = math.floor(active_map.elevation[y][x] * 255)
                tile_marker.fill((value, value, value))
                raw_maps[0].blit(tile_marker, [x, y])
    if not exclusive or exclusive == "temp":
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
                tile_marker.fill(temp_gradient[value])
                raw_maps[1].blit(tile_marker, [x, y])
    if not exclusive or exclusive == "moisture":
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
                tile_marker.fill(moisture_gradient[value])
                raw_maps[2].blit(tile_marker, [x, y])
    if not exclusive or exclusive == "biome":
        print("drawing biome map...")
        for y in range(height):
            for x in range(width):
                biome = active_map.game_tile_rows[y][x].biome
                tile_marker.fill(util.colors.biome_colors[biome])
                raw_maps[3].blit(tile_marker, [x, y])

        tile_marker.fill(util.colors.purple)
        for each in active_map.cities:
            # zoc_tiles = utilities.get_nearby_tiles(active_map, [each.column, each.row], 8)
            # for tile in zoc_tiles:
                # biome_map_image.blit(tile_marker, [tile.column, tile.row])
            raw_maps[3].blit(tile_marker, [each.column, each.row])
        tile_marker.fill(util.colors.red)
        for row in active_map.game_tile_rows:
            for tile in row:
                if tile.resource:
                    raw_maps[3].blit(tile_marker, [tile.column, tile.row])
    if not exclusive or exclusive == "city score":
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
            tile_marker.fill(score_gradient[normalized_value])
            raw_maps[5].blit(tile_marker, [site.tile.column, site.tile.row])
    if not exclusive or exclusive == "trade score":
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
            tile_marker.fill(score_gradient[normalized_value])
            raw_maps[4].blit(tile_marker, [site.tile.column, site.tile.row])
        print("largest score recorder: {0}".format(largest))
    if not exclusive or exclusive == "water flux":
        print("rendering water flux")
        max_flux = 0
        for each_row in active_map.game_tile_rows:
            for each_tile in each_row:
                if each_tile.water_flux[2] > max_flux:
                    max_flux = each_tile.water_flux[2]
        flux_gradient = {0: (0, 76, 229),
                         1: (24, 91, 206),
                         2: (48, 106, 184),
                         3: (72, 121, 161),
                         4: (96, 136, 139),
                         5: (120, 151, 116),
                         6: (144, 166, 94),
                         7: (168, 181, 71),
                         8: (192, 196, 49),
                         9: (216, 211, 26),
                         10: (241, 226, 4)}
        max_flux = active_map.river_cutoff * 1.25
        for y in range(height):
            for x in range(width):
                flux = active_map.game_tile_rows[y][x].water_flux[2]
                value = min(10, round((flux / max_flux) * 10))
                tile_marker.fill(flux_gradient[value])
                raw_maps[6].blit(tile_marker, [x, y])
        print("Max Water Flux: {0}".format(max_flux))


def prepare_map_surfaces(display_data):
    # prepares blank, properly sized, destination map surfaces
    display_width, display_height, display_scale = (display_data[0],
                                                    display_data[1],
                                                    display_data[2])
    if display_scale:
        display_width = 264
        display_height = 264

    map_surfaces = [pygame.Surface([display_width, display_height])
                    for i in range(7)]
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
    scaled_maps = prepare_map_surfaces(display_data)  # generate blank destination surfaces that are properly sized

    for i, raw_map in enumerate(raw_maps):
        pygame.transform.smoothscale(raw_map, (display_width, display_height), scaled_maps[i])
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


def display_update(screen, raw_maps, display_data, clock):
    scaled_maps = scale_maps(raw_maps, display_data)
    render_rotated_maps(screen, scaled_maps, display_data)
    render_map_labels(screen, scaled_maps, display_data)


def quit_check():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()


def input_loop(game_state, mgs, message="Press Enter to Continue"):
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
                enter_message = message_font.render("Please Wait...",
                                                    True,
                                                    util.colors.white)
            elif event.type == pygame.VIDEORESIZE:
                game_state.screen = pygame.display.set_mode((event.w, event.h),
                                                            pygame.RESIZABLE)
                game_state.screen_width = event.w
                game_state.screen_height = event.h

        game_state.screen.fill(util.colors.black)
        display_update(game_state.screen,
                       mgs.raw_maps,
                       mgs.display_data,
                       mgs.clock)

        game_state.screen.blit(enter_message,
                               [10, game_state.screen_height - 24])
        pygame.display.flip()


class MapgenState(object):
    def __init__(self, active_map: Map) -> None:
        self.active_map = active_map
        self.display_scale = False
        self.display_data = (self.width, self.height, self.display_scale)
        self.clock = pygame.time.Clock()
        self.raw_maps = self.initialize_raw_maps(self.width, self.height)
        self.map_accepted = False
        self.scaled_maps = scale_maps(self.raw_maps, self.display_data)

    @property
    def width(self):
        return self.active_map.width

    @property
    def height(self):
        return self.active_map.height

    @property
    def water_cutoff(self):
        return self.active_map.water_cutoff

    @property
    def max_resource_cluster_size(self):
        return self.active_map.max_resource_cluster_size

    def initialize_raw_maps(self, width, height):
        generate_blank_ocean_tiles(self.active_map)
        map_previews = [pygame.Surface([width, height])
                        for i in range(7)]
        clean_map_previews = []
        for each in map_previews:
            each.fill((110, 110, 110))
            each.set_colorkey(util.colors.key)
            each = each.convert_alpha()
            clean_map_previews.append(each)
        return clean_map_previews


def is_coastal(active_map, largest_water_body, site):
    neighbor_tiles = util.get_adjacent_tiles(site.tile, active_map)
    return (
        any(neighbor.biome in ['ocean', 'sea', 'shallows'] for neighbor in neighbor_tiles) and
        any(largest_water_body[neighbor.column, neighbor.row] == 1 for neighbor in neighbor_tiles))


def make_map(game_state, mgs: MapgenState):
    message_font = pygame.font.SysFont('Calibri', 14, True, False)
    generate_heightmap(mgs.active_map)
    adjust_landmass_height(mgs.active_map)
    infill_basins(mgs.active_map)

    render_raw_maps(mgs.active_map,
                    mgs.width,
                    mgs.height,
                    mgs.raw_maps,
                    'height')
    display_update(game_state.screen,
                   mgs.raw_maps,
                   mgs.display_data,
                   mgs.clock)

    mgs.active_map.temperature = generate_tempmap(mgs.width, mgs.height)
    mgs.active_map.moisture = generate_moisture_map(mgs.width,
                                                    mgs.height,
                                                    mgs.active_map.elevation,
                                                    mgs.water_cutoff)
    generate_biomes(mgs.active_map, mgs.water_cutoff)
    generate_terrain(mgs.active_map)
    generate_rivers(mgs.active_map, mgs.water_cutoff)
    place_resources(mgs.active_map, mgs.max_resource_cluster_size)
    print("map complete")

    for map_type in ('height', 'temp', 'moisture', 'water flux', 'biome'):
        render_raw_maps(mgs.active_map,
                        mgs.width,
                        mgs.height,
                        mgs.raw_maps,
                        map_type)

    display_update(game_state.screen,
                   mgs.raw_maps,
                   mgs.display_data,
                   mgs.clock)

    input_loop(game_state, mgs, "Press Enter to Survey City Sites")

    print("surveying city candidates...")
    for row in mgs.active_map.game_tile_rows:
        for tile in row:
            mgs.active_map.all_tiles.append(tile)
    all_sites = [city.Site(tile, mgs.active_map)
                 for tile in mgs.active_map.all_tiles]
    viable_sites = list(filter(city.Site.is_viable, all_sites))
    largest_water_body = city.cull_interior_watermasses(mgs.active_map)
    coastal_sites = list(filter(lambda x: is_coastal(mgs.active_map,
                                                     largest_water_body,
                                                     x), viable_sites))
    print(len(coastal_sites))
    for site in all_sites:
        if site.tile.biome not in ('ocean', 'shallows', 'sea', 'lake'):
            site.update_scores(mgs.active_map, coastal_sites)

    render_raw_maps(mgs.active_map,
                    mgs.width,
                    mgs.height,
                    mgs.raw_maps,
                    "trade score",
                    all_sites)
    render_raw_maps(mgs.active_map,
                    mgs.width,
                    mgs.height,
                    mgs.raw_maps,
                    "city score",
                    all_sites)
    display_update(game_state.screen,
                   mgs.raw_maps,
                   mgs.display_data,
                   mgs.clock)
    input_loop(game_state, mgs, "Map Surveyed, Press Enter to Place Cities")

    print("placing cities...")
    for ii in range(mgs.active_map.number_of_cities):
        quit_check()
        print("Debug A")
        city.add_new_city(mgs.active_map, viable_sites, coastal_sites)

        start = time.time()
        for site in viable_sites:
            site.update_scores(mgs.active_map, coastal_sites)
        elapsed = time.time() - start
        print('scoring time: {}s'.format(round(elapsed, 3)))

        print("city placed: {0} / {1}".format(len(mgs.active_map.cities),
                                              mgs.active_map.number_of_cities))
        city_counter = message_font.render("Cities Placed:".format(len(mgs.active_map.cities),
                                                                         mgs.active_map.number_of_cities),
                                           True,
                                           util.colors.white)
        n_cities_placed = message_font.render("{0} / {1}".format(str(len(mgs.active_map.cities)), str(mgs.active_map.number_of_cities)),
                                              True,
                                              util.colors.light_green)
        game_state.screen.fill(util.colors.black)
        render_raw_maps(mgs.active_map,
                        mgs.width,
                        mgs.height,
                        mgs.raw_maps,
                        "trade score",
                        all_sites)
        render_raw_maps(mgs.active_map,
                        mgs.width,
                        mgs.height,
                        mgs.raw_maps,
                        "city score",
                        viable_sites)
        display_update(game_state.screen, mgs.raw_maps, mgs.display_data, mgs.clock)
        game_state.screen.blit(city_counter,
                               [10, game_state.screen_height - 24])
        game_state.screen.blit(n_cities_placed,
                               [90, game_state.screen_height - 24])
        pygame.display.flip()

    print("cities placed!")
    sound.chime.play()
    region.grow_cities(mgs.active_map)


def map_generation(game_state, active_map: Map):
    mgs = MapgenState(active_map)
    input_loop(game_state, mgs)
    render_map_labels(game_state.screen, mgs.scaled_maps, mgs.display_data)
    display_update(game_state.screen, mgs.raw_maps, mgs.display_data, mgs.clock)
    make_map(game_state, mgs)
    while not mgs.map_accepted:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mgs.map_accepted = True

    active_map.paint_background_tiles(active_map.game_tile_rows)
    active_map.paint_terrain_layer(active_map.game_tile_rows)
    active_map.paint_resource_layer(active_map.game_tile_rows)
    active_map.paint_building_layer(active_map.game_tile_rows)

    scaled_maps = scale_maps(mgs.raw_maps, mgs.display_data)
    active_map.biome_map_preview = pygame.Surface([140, 140])
    pygame.transform.smoothscale(scaled_maps[3],
                                 (140, 140),
                                 active_map.biome_map_preview)
    active_map.biome_map_preview.set_colorkey(util.colors.key)
    active_map.biome_map_preview = active_map.biome_map_preview.convert_alpha()
