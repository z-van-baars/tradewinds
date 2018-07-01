from opensimplex import OpenSimplex
import utilities
import math
import random
import queue
import construct
from game_tile import GameTile
import pygame
import city
import artikel
import time

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
                    equatorial_distances.append(utilities.distance(each[0], each[1], x, y))
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


def generate_rivers(active_map, water_cutoff):
    print("running rivers...")
    river_cutoff = 1000
    moisture_layers = queue.PriorityQueue()
    for y_row in active_map.game_tile_rows:
        for tile in y_row:
            elevation = active_map.elevation[tile.row][tile.column]
            if active_map.elevation[tile.row][tile.column] > water_cutoff:
                moisture_layers.put((-elevation, tile))
    while not moisture_layers.empty():
        moisture, tile = moisture_layers.get()
        moisture = -moisture
        neighbors = utilities.get_adjacent_tiles(tile, active_map)
        flow_neighbors = []
        for each_tile in neighbors:
            if active_map.elevation[each_tile.row][each_tile.column] < active_map.elevation[tile.row][tile.column]:
                flow_neighbors.append(each_tile)
        if len(flow_neighbors) == 0:
            tile.water_flux = tile.water_in
            if tile.water_flux >= river_cutoff:
                tile.biome = "ocean"
        else:
            lowest_neighbor = tile
            for each_neighbor in flow_neighbors:
                if active_map.elevation[each_neighbor.row][each_neighbor.column] < active_map.elevation[lowest_neighbor.row][lowest_neighbor.column]:
                    lowest_neighbor = each_neighbor
            assert lowest_neighbor != tile
            tile.water_out = tile.water_in + active_map.moisture[tile.row][tile.column]
            lowest_neighbor.water_in = tile.water_in + active_map.moisture[tile.row][tile.column]
            tile.water_flux = tile.water_in + tile.water_out
    for each_row in active_map.game_tile_rows:
        for each_tile in each_row:
            if each_tile.water_flux > river_cutoff and each_tile.biome != "ocean":
                each_tile.biome = "river"


def generate_blank_grass_tiles(active_map):
    active_map.game_tile_rows = []
    for y_row in range(active_map.number_of_rows):
        this_row = []
        for x_column in range(active_map.number_of_columns):
            this_row.append(GameTile(x_column, y_row, "grass"))
        active_map.game_tile_rows.append(this_row)


def generate_blank_ocean_tiles(active_map):
    active_map.game_tile_rows = []
    for y_row in range(active_map.number_of_rows):
        this_row = []
        for x_column in range(active_map.number_of_columns):
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


def generate_land(active_map, water_cutoff):
    biome_temps, biome_moisture = get_biome_parameters()
    for y_row in active_map.game_tile_rows:
        for tile in y_row:
            if active_map.elevation[tile.row][tile.column] >= water_cutoff:
                temperature = active_map.temperature[tile.row][tile.column]
                moisture = active_map.moisture[tile.row][tile.column]
                biome = pick_biome(biome_temps[temperature], biome_moisture[moisture])
                if biome == "plains":
                    if active_map.moisture[tile.row][tile.column] >= 55:
                        biome = "wet plains"
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
    tiles_in_radius = utilities.get_nearby_tiles(active_map, [tile.row, tile.column], 5)
    for each_tile in tiles_in_radius:
        if tile.resource:
            return False
    return True


def pick_random_location(active_map):
    selected = False
    while not selected:
        tile_xy = utilities.get_random_coordinates(0, active_map.width - 1, 0, active_map.height - 1)
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

        nearby_tiles = utilities.get_nearby_tiles(active_map, [tile.row, tile.column], 5)
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


def render_raw_maps(active_map, width, height, raw_maps, exclusive=None):
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
                tile_marker.fill(utilities.colors.biome_colors[biome])
                raw_maps[3].blit(tile_marker, [x, y])

        tile_marker.fill(utilities.colors.purple)
        for each in active_map.cities:
            # zoc_tiles = utilities.get_nearby_tiles(active_map, [each.column, each.row], 8)
            # for tile in zoc_tiles:
                # biome_map_image.blit(tile_marker, [tile.column, tile.row])
            raw_maps[3].blit(tile_marker, [each.column, each.row])
        tile_marker.fill(utilities.colors.red)
        for row in active_map.game_tile_rows:
            for tile in row:
                if tile.resource:
                    raw_maps[3].blit(tile_marker, [tile.column, tile.row])
    if not exclusive or exclusive == "water flux":
        print("rendering water flux")
        max_flux = 0
        for each_row in active_map.game_tile_rows:
            for each_tile in each_row:
                if each_tile.water_flux > max_flux:
                    max_flux = each_tile.water_flux
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
        for y in range(height):
            for x in range(width):
                flux = active_map.game_tile_rows[y][x].water_flux
                value = min(10, round((flux / max_flux) * 10))
                tile_marker.fill(flux_gradient[value])
                raw_maps[6].blit(tile_marker, [x, y])
        print("Max Water Flux: {0}".format(max_flux))
    if not exclusive or exclusive == "city score":
        print("rendering city score map")
        max_score = 160
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
        for y in range(height):
            for x in range(width):
                score = active_map.city_score[y][x]
                value = min(10, round((score / max_score) * 10))
                if score > largest:
                    largest = score
                tile_marker.fill(score_gradient[value])
                raw_maps[5].blit(tile_marker, [x, y])
        # print("largest score recorder: {0}".format(largest))


def map_generation(active_map):
    clock = pygame.time.Clock()
    accepted = False
    width = active_map.width
    height = active_map.height
    screen = pygame.display.set_mode([1600, 1000])
    water_cutoff = 0.5
    max_resource_cluster_size = 5

    display_scale = False

    def reset_previews(width, height):
        generate_blank_ocean_tiles(active_map)
        map_previews = [pygame.Surface([width, height]),
                        pygame.Surface([width, height]),
                        pygame.Surface([width, height]),
                        pygame.Surface([width, height]),
                        pygame.Surface([width, height]),
                        pygame.Surface([width, height]),
                        pygame.Surface([width, height])]
        clean_map_previews = []
        for each in map_previews:
            each.fill((110, 110, 110))
            each.set_colorkey(utilities.colors.key)
            each = each.convert_alpha()
            clean_map_previews.append(each)
        return clean_map_previews

    def reset_resized(display_scale, width, height):
        width = width
        height = height
        if display_scale:
            width = 264
            height = 264
        map_previews = [pygame.Surface([width, height]),
                        pygame.Surface([width, height]),
                        pygame.Surface([width, height]),
                        pygame.Surface([width, height]),
                        pygame.Surface([width, height]),
                        pygame.Surface([width, height]),
                        pygame.Surface([width, height])]
        clean_map_previews_scaled = []
        for each in map_previews:
            each.fill((110, 110, 110))
            each.set_colorkey(utilities.colors.key)
            each = each.convert_alpha()
            clean_map_previews_scaled.append(each)
        return clean_map_previews_scaled
    raw_maps = reset_previews(width, height)
    scaled_maps = reset_resized(display_scale, width, height)

    rotation = (-45)
    if display_scale:
        c = math.sqrt(264 ** 2 + 264 ** 2)
    else:
        c = pygame.transform.rotate(raw_maps[0], rotation).get_width()
    while not accepted:
        screen.blit(pygame.transform.rotate(scaled_maps[0], rotation), [0, 0])  # heightmap
        screen.blit(pygame.transform.rotate(scaled_maps[1], rotation), [c + 5, 0])  # tempmap
        screen.blit(pygame.transform.rotate(scaled_maps[2], rotation), [0, c + 5])  # moisture map
        screen.blit(pygame.transform.rotate(scaled_maps[3], rotation), [c + 5, c + 5])  # biome map with cities marked
        screen.blit(pygame.transform.rotate(scaled_maps[4], rotation), [c * 2 + 10, 0])  # trade connectivity map
        screen.blit(pygame.transform.rotate(scaled_maps[5], rotation), [c * 2 + 10, c + 5])  # city score map
        screen.blit(pygame.transform.rotate(scaled_maps[6], rotation), [c * 3 + 15, 0])  # water flux map
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    raw_maps = reset_previews(width, height)
                    scaled_maps = reset_resized(display_scale, width, height)
                    generate_heightmap(active_map)
                    active_map.temperature = generate_tempmap(width, height)
                    active_map.moisture = generate_moisture_map(width, height, active_map.elevation, water_cutoff)
                    generate_land(active_map, water_cutoff)
                    generate_terrain(active_map)
                    generate_rivers(active_map, water_cutoff)
                    place_resources(active_map, max_resource_cluster_size)
                    print("map complete")
                    for map_type in ('height', 'temp', 'moisture', 'water flux', 'biome'):
                        render_raw_maps(active_map, width, height, raw_maps, map_type)
                    display_width = width
                    display_height = height
                    if display_scale:
                        display_width = 264
                        display_height = 264
                    pygame.transform.smoothscale(raw_maps[0], (display_width, display_height), scaled_maps[0])
                    pygame.transform.smoothscale(raw_maps[1], (display_width, display_height), scaled_maps[1])
                    pygame.transform.smoothscale(raw_maps[2], (display_width, display_height), scaled_maps[2])
                    pygame.transform.smoothscale(raw_maps[3], (display_width, display_height), scaled_maps[3])
                    pygame.transform.smoothscale(raw_maps[4], (display_width, display_height), scaled_maps[4])
                    pygame.transform.smoothscale(raw_maps[5], (display_width, display_height), scaled_maps[5])
                    pygame.transform.smoothscale(raw_maps[6], (display_width, display_height), scaled_maps[6])

                    screen.blit(pygame.transform.rotate(scaled_maps[0], rotation), [0, 0])  # heightmap
                    screen.blit(pygame.transform.rotate(scaled_maps[1], rotation), [c + 5, 0])  # tempmap
                    screen.blit(pygame.transform.rotate(scaled_maps[2], rotation), [0, c + 5])  # moisture map
                    screen.blit(pygame.transform.rotate(scaled_maps[3], rotation), [c + 5, c + 5])  # biome map with cities marked
                    screen.blit(pygame.transform.rotate(scaled_maps[4], rotation), [c * 2 + 10, 0])  # trade connectivity map
                    screen.blit(pygame.transform.rotate(scaled_maps[5], rotation), [c * 2 + 10, c + 5])  # city score map
                    screen.blit(pygame.transform.rotate(scaled_maps[6], rotation), [c * 3 + 15, 0])  # water flux map
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(0.5)

                    print("surveying city candidates...")
                    zone_of_control, food_score, temperature_score, resource_score, city_score, city_candidates = city.survey_city_sites(active_map)
                    number_of_cities = math.floor(math.sqrt(active_map.width * active_map.height) / 5)
                    active_map.city_score = city_score
                    cities = []

                    number_of_cities = 25
                    print("placing cities...")
                    for ii in range(number_of_cities):
                        active_map.cities = city.add_new_city(active_map,
                                                              city_candidates,
                                                              zone_of_control,
                                                              food_score,
                                                              temperature_score,
                                                              resource_score,
                                                              cities)
                        print("city placed: {0} / {1}".format(len(cities), number_of_cities))
                        render_raw_maps(active_map, width, height, raw_maps, "city score")
                        display_width = width
                        display_height = height
                        if display_scale:
                            display_width = 264
                            display_height = 264
                        pygame.transform.smoothscale(raw_maps[0], (display_width, display_height), scaled_maps[0])
                        pygame.transform.smoothscale(raw_maps[1], (display_width, display_height), scaled_maps[1])
                        pygame.transform.smoothscale(raw_maps[2], (display_width, display_height), scaled_maps[2])
                        pygame.transform.smoothscale(raw_maps[3], (display_width, display_height), scaled_maps[3])
                        pygame.transform.smoothscale(raw_maps[4], (display_width, display_height), scaled_maps[4])
                        pygame.transform.smoothscale(raw_maps[5], (display_width, display_height), scaled_maps[5])
                        pygame.transform.smoothscale(raw_maps[6], (display_width, display_height), scaled_maps[6])

                        screen.blit(pygame.transform.rotate(scaled_maps[0], rotation), [0, 0])  # heightmap
                        screen.blit(pygame.transform.rotate(scaled_maps[1], rotation), [c + 5, 0])  # tempmap
                        screen.blit(pygame.transform.rotate(scaled_maps[2], rotation), [0, c + 5])  # moisture map
                        screen.blit(pygame.transform.rotate(scaled_maps[3], rotation), [c + 5, c + 5])  # biome map with cities marked
                        screen.blit(pygame.transform.rotate(scaled_maps[4], rotation), [c * 2 + 10, 0])  # trade connectivity map
                        screen.blit(pygame.transform.rotate(scaled_maps[5], rotation), [c * 2 + 10, c + 5])  # city score map
                        screen.blit(pygame.transform.rotate(scaled_maps[6], rotation), [c * 3 + 15, 0])  # water flux map
                        pygame.display.flip()
                        clock.tick(60)
                        time.sleep(0.5)
                    active_map.cities = cities
                    print("cities placed!")
                elif event.key == pygame.K_SPACE:
                    accepted = True
        pygame.display.flip()
        clock.tick(60)

    active_map.paint_background_tiles(active_map.game_tile_rows)
    active_map.paint_terrain_layer(active_map.game_tile_rows)
    active_map.paint_resource_layer(active_map.game_tile_rows)
    active_map.paint_building_layer(active_map.game_tile_rows)

    active_map.biome_map_preview = pygame.Surface([140, 140])
    pygame.transform.smoothscale(scaled_maps[3], (140, 140), active_map.biome_map_preview)
    active_map.biome_map_preview.set_colorkey(utilities.colors.key)
    active_map.biome_map_preview = active_map.biome_map_preview.convert_alpha()
