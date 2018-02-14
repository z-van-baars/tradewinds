from opensimplex import OpenSimplex
import utilities
import math
import random
import queue
import construct
from game_tile import GameTile
import pygame



pygame.init()
pygame.display.set_mode([0, 0])


def generate_heightmap(active_map):
    gen = OpenSimplex(random.randrange(100000))

    def noise(nx, ny):
        # rescale from -1.0:+1/0 to 0.0:1.0
        return gen.noise2d(nx, ny) / 2.0 + 0.5

    elevation = []
    width = len(active_map.game_tile_rows[0])
    height = len(active_map.game_tile_rows)
    for y in range(height):
        elevation.append([])
        for x in range(width):
            # print(x, y)
            nx = x / width - 0.5
            ny = y / height - 0.5
            # print(nx, ny)
            new = (1.00 * noise(4 * nx, 4 * ny) +
                   0.5 * noise(8 * nx, 8 * ny) +
                   0.25 * noise(32 * nx, 32 * ny) +
                   0.13 * noise(64 * nx, 64 * ny))
            new = new / (1 + 0.5 + 0.25 + 0.13)
            elevation[y].append(new)
    active_map.elevation = elevation


def generate_tempmap(width, height):
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
        temp = 1 + distance_modifier * equator_hotness - distance_modifier * pole_coldness
        new_temperature = min(math.floor(max((temp + (temp * new) * noise_strength) * abs(1.0 - noise_strength), 0) * 100), 100)
        return new_temperature

    number_of_points = math.floor(math.sqrt(math.sqrt(width * height)))
    print(number_of_points)
    slope = (width / number_of_points, height / number_of_points)
    print(slope)
    xx = 0
    yy = height
    equator = [(xx, yy)]
    for e in range(number_of_points + 2):
        print(xx, yy)
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
        if 0 <= t < 30:
            temp = "cold"
        elif 30 <= t < 60:
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
    biomes = {"cold": {"very dry": "tundra",
                       "dry": "tundra",
                       "wet": "taiga",
                       "very wet": "ice"},
              "cool": {"very dry": "taiga",
                       "dry": "grassland",
                       "wet": "grassland",
                       "very wet": "grassland"},
              "warm": {"very dry": "plains",
                       "dry": "grassland",
                       "wet": "grassland",
                       "very wet": "grassland"},
              "hot": {"very dry": "desert",
                      "dry": "plains",
                      "wet": "plains",
                      "very wet": "grassland"}}

    return(biomes[temperature][moisture])


def generate_land(active_map, water_cutoff):
    biome_temps, biome_moisture = get_biome_parameters()
    for y_row in active_map.game_tile_rows:
        for tile in y_row:
            if active_map.elevation[tile.row][tile.column] >= water_cutoff:
                temperature = active_map.temperature[tile.row][tile.column]
                moisture = active_map.moisture[tile.row][tile.column]
                biome = pick_biome(biome_temps[temperature], biome_moisture[moisture])
                tile.biome = biome


def generate_terrain(active_map):
    hill_cutoff = 0.65
    mountain_cutoff = 0.75
    for y_row in active_map.game_tile_rows:
        for tile in y_row:
            if mountain_cutoff > active_map.elevation[tile.row][tile.column] >= hill_cutoff:
                tile.terrain = "hill"
            elif active_map.elevation[tile.row][tile.column] >= hill_cutoff:
                tile.terrain = "mountain"


def generate_land_legacy(active_map):
    def spread_contiguous_land(active_map, game_size, seed_tile):
        candidates = []
        candidates = utilities.get_adjacent_tiles(seed_tile, active_map)
        for each in candidates:
            print(each.column, each.row)
        for ll in range(game_size ** 5):
            spread_choice = None
            while not spread_choice:
                spread_choice = candidates.pop(random.randrange(len(candidates)))
                if spread_choice.terrain == "grass":
                    spread_choice = None
                print(spread_choice)
            spread_choice.terrain = "grass"
            new_candidates = utilities.get_adjacent_tiles(spread_choice, active_map)
            print(active_map)
            for candidate in new_candidates:
                if candidate not in candidates and candidate.terrain == "ocean":
                    candidates.append(candidate)

    game_size = math.floor(math.sqrt(math.sqrt(active_map.number_of_columns * active_map.number_of_rows)) / 2)
    islands_to_generate = game_size
    print(islands_to_generate)
    island_seeds = []
    for island in range(islands_to_generate):
        coordinates_chosen = False
        while not coordinates_chosen:
            random_xy = utilities.get_random_coordinates(0, active_map.number_of_columns - 1, 0, active_map.number_of_rows - 1)
            if not active_map.game_tile_rows[random_xy[1]][random_xy[0]].terrain == "grass":
                coordinates_chosen = True
                island_seeds.append(random_xy)
    for seed in island_seeds:
        active_map.game_tile_rows[seed[1]][seed[0]].terrain = "grass"
    for seed in island_seeds:
        spread_contiguous_land(active_map, game_size, active_map.game_tile_rows[seed[1]][seed[0]])


def generate_forests(active_map, width, height):
    number_of_forests = math.floor(math.sqrt(width * height))
    for ii in range(number_of_forests):
        new_forest_center = False
        while not new_forest_center:
            new_forest_center = utilities.get_random_coordinates(0, width - 1, 0, height - 1)
            if active_map.game_tile_rows[new_forest_center[1]][new_forest_center[0]].is_occupied():
                new_forest_center = False
        forest_tiles = utilities.get_nearby_tiles(active_map, new_forest_center, math.floor(math.sqrt(number_of_forests) / 2))
        forest_size = random.randint(math.floor(math.sqrt(number_of_forests)), math.floor(math.sqrt(number_of_forests) * 2))
        for jj in range(forest_size):
            new_tree_xy = random.choice(forest_tiles)
            if active_map.game_tile_rows[new_tree_xy.row][new_tree_xy.column].is_occupied():
                new_tree_xy = False
            if new_tree_xy:
                new_tree = construct.Tree(new_tree_xy.column, new_tree_xy.row, active_map)
                active_map.terrain.append(new_tree)
                active_map.game_tile_rows[new_tree_xy.row][new_tree_xy.column].construct = new_tree


def map_generation(active_map):
    # generate_land(active_map)
    clock = pygame.time.Clock()
    accepted = False
    width = active_map.width
    height = active_map.height
    screen = pygame.display.set_mode([1600, 1000])
    water_cutoff = 0.5

    def reset_previews():
        generate_blank_ocean_tiles(active_map)
        height_map_image = pygame.Surface([width, height])
        height_map_image.fill((110, 110, 110))
        height_map_image.set_colorkey(utilities.colors.key)
        height_map_image.convert_alpha()
        temp_map_image = pygame.Surface([width, height])
        temp_map_image.fill((110, 110, 110))
        temp_map_image.set_colorkey(utilities.colors.key)
        temp_map_image.convert_alpha()
        moisture_map_image = pygame.Surface([width, height])
        moisture_map_image.fill((110, 110, 110))
        moisture_map_image.set_colorkey(utilities.colors.key)
        moisture_map_image.convert_alpha()
        biome_preview_image = pygame.Surface([width, height])
        biome_preview_image.fill((110, 110, 110))
        biome_preview_image.set_colorkey(utilities.colors.key)
        biome_preview_image.convert_alpha()
        return height_map_image, temp_map_image, moisture_map_image, biome_preview_image
    height_map_image, temp_map_image, moisture_map_image, biome_preview_image = reset_previews()
    tile_marker = pygame.Surface([1, 1])
    tile_marker.fill((0, 0, 0))
    rotation = (-45)
    c = pygame.transform.rotate(height_map_image, rotation).get_width()
    while not accepted:
        screen.blit(pygame.transform.rotate(height_map_image, rotation), [0, 0])
        screen.blit(pygame.transform.rotate(temp_map_image, rotation), [c + 5, 0])
        screen.blit(pygame.transform.rotate(moisture_map_image, rotation), [0, c + 5])
        screen.blit(pygame.transform.rotate(biome_preview_image, rotation), [c + 5, c + 5])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("generating heightmap...")
                    reset_previews()
                    generate_heightmap(active_map)
                    active_map.temperature = generate_tempmap(width, height)
                    active_map.moisture = generate_moisture_map(width, height, active_map.elevation, water_cutoff)
                    generate_land(active_map, water_cutoff)
                    generate_terrain(active_map)
                    print("drawing heightmap...")
                    for y in range(height):
                        for x in range(width):
                            value = math.floor(active_map.elevation[y][x] * 255)
                            tile_marker.fill((value, value, value))
                            height_map_image.blit(tile_marker, [x, y])

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
                    print("drawing temperature map...")
                    for y in range(height):
                        for x in range(width):
                            value = math.floor(max(0, (active_map.temperature[y][x] - 1)) * 0.1)
                            tile_marker.fill(temp_gradient[value])
                            temp_map_image.blit(tile_marker, [x, y])
                    print("drawing moisture map...")
                    for y in range(height):
                        for x in range(width):
                            value = math.floor(active_map.moisture[y][x] * 2.55)
                            tile_marker.fill((0, 0, value))
                            moisture_map_image.blit(tile_marker, [x, y])
                    print("drawing biome map...")
                    for y in range(height):
                        for x in range(width):
                            biome = active_map.game_tile_rows[y][x].biome
                            tile_marker.fill(utilities.colors.biome_colors[biome])
                            biome_preview_image.blit(tile_marker, [x, y])
                    print("map complete")

                elif event.key == pygame.K_SPACE:
                    accepted = True
        pygame.display.flip()
        clock.tick(60)



    # active_map.generate_resources(active_map.width, active_map.height)
    active_map.paint_background_tiles(active_map.game_tile_rows)
    active_map.paint_terrain_layer(active_map.game_tile_rows)
    # active_map.paint_resources()
    # active_map.paint_buildings()
