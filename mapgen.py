from opensimplex import OpenSimplex
import utilities as util
import production as prod
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
import nation
import mapgen_render as mgr
import ships

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
            # 'a' pushes all land up
            # higher value means more land but also chance of edge touching
            a = 0.04
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
        """modified perlin noise generator
        resulting values are normalized into "temperature" """
        nx = x / width - 0.5
        ny = y / height - 0.5
        new = (1.0 * noise(noisiness * nx, noisiness * ny))
        new = new / (noise_strength)
        max_distance = math.sqrt(width * height)
        distance_modifier = (pole_distances[y][x] / max_distance)
        temp = (1.0 +
                distance_modifier *
                equator_hotness -
                distance_modifier *
                pole_coldness)
        new_temperature = min(
            math.floor(
                max((temp + (temp * new) * noise_strength) *
                    abs(1.0 - noise_strength), 0) * 100), 100)
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
            new_temperature = get_temperature(
                equator_hotness,
                pole_coldness,
                noise_strength,
                noisiness)
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
                new_moisture = min(
                    100,
                    new * 100 - (new * 75) * (elevation[y][x] - water_cutoff * 1.5))
            moisture[y].append(math.floor(new_moisture))

    return moisture


def classify_masses(active_map):
    print('classifying landmasses...')
    water_array = np.ones((active_map.width, active_map.height))
    for row in active_map.game_tile_rows:
        for tile in row:
            if active_map.elevation[tile.row][tile.column] >= active_map.mgp.water_cutoff:
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
            active_map.elevation[each_tile.row][each_tile.column] = min(
                active_map.mgp.water_cutoff + 0.01, (
                    active_map.elevation[each_tile.row][each_tile.column] + 0.01))
            e = active_map.elevation[each_tile.row][each_tile.column]
            if e < active_map.mgp.water_cutoff + 0.01:
                raising = True


def infill_basins(active_map):
    print("filling basins...")
    water_cutoff = active_map.mgp.water_cutoff

    # builds a stack of layer tuples to iterate through
    z_layers = queue.PriorityQueue()
    for y_row in active_map.game_tile_rows:
        for tile in y_row:
            elevation = active_map.elevation[tile.row][tile.column]
            if active_map.elevation[tile.row][tile.column] > water_cutoff:
                # inverting the highest elevation - get() operation takes lowest float
                z_layers.put((-elevation, tile))

    # works from the highest z(elevation) to the lowest
    # adding water flux to lower tiles cumulatively
    while not z_layers.empty():
        elevation, previous_tile = z_layers.get()
        neighbors = util.get_adjacent_tiles(tile, active_map)

        # builds a list of neighbors who are at a lower Z level
        flowable_neighbors = []
        # backup list in case we bottom out and need to fill in a lake
        all_neighbors = []
        for each_tile in neighbors:
            e = active_map.elevation[each_tile.row][each_tile.column]
            if e < active_map.elevation[previous_tile.row][previous_tile.column]:
                flowable_neighbors.append((e, each_tile))
            all_neighbors.append((e, each_tile))

        # if no neighboring tile is lower, cease flow
        # turn this tile into a SHALLOWS tile / LAKE
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
                            frontier.append((
                                active_map.elevation[neighbor.row][neighbor.column],
                                neighbor))
                            frontier = sorted(frontier)
                for tile_to_raise in tiles_to_raise:
                    active_map.elevation[tile_to_raise.row][tile_to_raise.column] = last_addition_elevation


def generate_rivers(active_map, water_cutoff):
    print("running rivers...")
    river_cutoff = active_map.mgp.river_cutoff

    # builds a stack of layer tuples to iterate through
    moisture_layers = queue.PriorityQueue()
    for y_row in active_map.game_tile_rows:
        for tile in y_row:
            elevation = active_map.elevation[tile.row][tile.column]
            if active_map.elevation[tile.row][tile.column] > water_cutoff:
                # inverting the highest elevation brings it to the top
                # of the queue for the get() operator
                moisture_layers.put((-elevation, tile))

    # works from the highest z(elevation) to the lowest
    # adding water flux to lower tiles cumulatively
    while not moisture_layers.empty():
        elevation, tile = moisture_layers.get()
        neighbors = util.get_adjacent_tiles(tile, active_map)

        # builds a list of neighbors who are at a lower Z level
        flowable_neighbors = []
        # backup list in case we bottom out and need to fill in a lake
        all_neighbors = []
        for each_tile in neighbors:
            if active_map.elevation[each_tile.row][each_tile.column] < active_map.elevation[tile.row][tile.column]:
                flowable_neighbors.append((active_map.elevation[each_tile.row][each_tile.column], each_tile))
            all_neighbors.append((active_map.elevation[each_tile.row][each_tile.column], each_tile))

        # if no neighboring tile is lower:
        # cease to flow, turn this tile into a SHALLOWS tile / LAKE
        # repeat and expand the lake upward until we have an appropriate
        # exit vector lower than the entry vector
        if len(flowable_neighbors) == 0:
            water_in = tile.water_flux[0]
            water_out = water_in
            total_flux = (water_in + water_out +
                          active_map.moisture[tile.row][tile.column])
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
                    last_addition.water_flux = (max(water_in,
                                                    last_addition.water_flux[0]),
                                                max(water_out,
                                                    last_addition.water_flux[1]),
                                                max(total_flux,
                                                    last_addition.water_flux[2]))
                    new_neighbors = util.get_adjacent_tiles(last_addition, active_map)
                    for neighbor in new_neighbors:
                        if (active_map.elevation[neighbor.row][neighbor.column], neighbor) not in frontier:
                            if neighbor not in tiles_filled:
                                frontier.append(
                                    (active_map.elevation[neighbor.row][neighbor.column],
                                     neighbor))
                                frontier = sorted(frontier)
                frontier[0][1].water_flux = (water_in, 0, 0)
                frontier[0][1].water_source = (
                    [util.get_neighbor_position(frontier[0][1], last_addition)],
                    0)

        # if we have >=1 lower tile, add our collected water flux to the lowest
        else:
            lowest_neighbor = sorted(flowable_neighbors)[0][1]

            water_in, water_out, total_flux = tile.water_flux
            # add incoming water flux to local moisture and send it out
            water_out = water_in + active_map.moisture[tile.row][tile.column]
            total_flux = water_in + water_out
            tile.water_source = (
                tile.water_source[0],
                util.get_neighbor_position(tile, lowest_neighbor))
            lowest_neighbor.water_flux = (
                water_out + lowest_neighbor.water_flux[0],
                0,
                0)
            if total_flux > river_cutoff:
                lowest_neighbor.water_source = (
                    lowest_neighbor.water_source[0] + [util.get_neighbor_position(
                        lowest_neighbor,
                        tile)],
                    0)

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


def set_biomes(active_map, water_cutoff):
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
                if (tile.biome != 'lake' and
                    tile.terrain is not any(["low hill",
                                             "hill",
                                             "low mountain",
                                             "mountain"])):
                    if tile.water_flux[2] > active_map.mgp.river_cutoff:
                        tile.terrain = "river"


def check_for_existing_resource(active_map, tile):
    tiles_in_radius = util.get_nearby_tiles(active_map, [tile.row, tile.column], 5)
    for each_tile in tiles_in_radius:
        if tile.resource:
            return False
    return True


def pick_random_location(active_map):
    selected = False
    while not selected:
        tile_xy = util.get_random_coordinates(
            0, active_map.width - 1,
            0, active_map.height - 1)
        tile = active_map.game_tile_rows[tile_xy[1]][tile_xy[0]]
        if check_for_existing_resource(active_map, tile):
            selected = True
    return tile


def pick_from_available_resources(active_map, tile):
    possible_resources = artikel.possible_resources[tile.terrain][tile.biome]
    return(random.choice(possible_resources))


def place_resources(active_map):
    max_retries = 5
    print("placing resources...")
    print("number of clusters: {0}".format(active_map.mgp.number_of_clusters))
    for ii in range(active_map.mgp.number_of_clusters):
        cluster_size = max(random.randint(1, active_map.mgp.max_cluster_size),
                           random.randint(1, active_map.mgp.max_cluster_size))
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
    # turns an input dict 'city scores' into an output array 'city score array'
    city_score_array = []

    for y in range(active_map.height):
        new_row = []
        for x in range(active_map.width):
            new_row.append(0)
        city_score_array.append(new_row)
    for site, score in city_scores.items():
        active_map.city_score[site.row][site.column] = score
    return city_score_array


class MapgenState(object):
    def __init__(self, active_map: Map) -> None:
        self.active_map = active_map
        self.display_scale = False
        self.display_data = (self.width, self.height, self.display_scale)
        self.clock = pygame.time.Clock()
        self.map_accepted = False

    @property
    def width(self):
        return self.active_map.width

    @property
    def height(self):
        return self.active_map.height

    @property
    def water_cutoff(self):
        return self.active_map.mgp.water_cutoff

    @property
    def max_resource_cluster_size(self):
        return self.active_map.mgp.max_resource_cluster_size

    def initialize_raw_maps(self, width, height):
        generate_blank_ocean_tiles(self.active_map)
        map_previews = [pygame.Surface([width, height])
                        for i in range(8)]
        clean_map_previews = []
        for each in map_previews:
            each.fill((110, 110, 110))
            each.set_colorkey(util.colors.key)
            each = each.convert_alpha()
            clean_map_previews.append(each)
        return clean_map_previews


def is_coastal(active_map, largest_water_body, site):
    neighbor_tiles = util.get_adjacent_tiles(site.tile, active_map)
    return (any(neighbor.biome in (
        ['ocean', 'sea', 'shallows']) for neighbor in neighbor_tiles) and
        any(largest_water_body[neighbor.column, neighbor.row] == 1
            for neighbor in neighbor_tiles))


def survey_city_sites(game_state):
    active_map = game_state.active_map
    all_sites = []
    viable_sites = []
    sorted_sites = queue.PriorityQueue()
    print("surveying city candidates...")
    all_sites = [city.Site(tile, active_map)
                 for tile in active_map.all_tiles]
    viable_sites = list(filter(city.Site.is_viable, all_sites))
    if active_map.largest_water_body is None:
        active_map.largest_water_body = city.cull_interior_watermasses(active_map)
    coastal_sites = list(filter(lambda x: is_coastal(active_map,
                                                     active_map.largest_water_body,
                                                     x), viable_sites))
    for site in viable_sites:
        site.update_scores(active_map, coastal_sites)
    for site in viable_sites:
        if site.city_score > 1:
            sorted_sites.put((-site.city_score, site.tile, site))
    return all_sites, viable_sites, sorted_sites


def spawn_cities(game_state):
    active_map = game_state.active_map
    message_font = pygame.font.SysFont('Calibri', 14, True, False)

    all_sites, viable_sites, sorted_sites = survey_city_sites(game_state)
    map_size_f = math.sqrt(
        math.sqrt(math.sqrt(
            game_state.active_map.width *
            game_state.active_map.height)))

    map_size_f = math.floor(map_size_f)
    active_map.render_raw_maps(['trade score', 'city score'], viable_sites)
    mgr.display_update(game_state.screen,
                       active_map.raw_maps,
                       active_map.display_data,
                       game_state.clock)
    mgr.input_loop(game_state,
                   "Initial Map Survey Complete, press Enter to spawn cities")
    for ii in range(active_map.mgp.number_of_cities):
        d = 0
        while d < random.randint(1 + map_size_f, math.floor(map_size_f * 1.5)):
            score, tile, site = sorted_sites.get()
            d = 1000
            for existing_city in game_state.active_map.cities:
                d1 = util.distance(
                    tile.column,
                    tile.row,
                    existing_city.column,
                    existing_city.row)
                if d1 < d:
                    d = d1
        new_city_name = city.get_city_name(active_map.cities)
        new_city = city.City(
            active_map,
            tile.column,
            tile.row,
            tile,
            new_city_name)
        active_map.add_city(new_city)

        game_state.screen.fill(util.colors.black)
        mgr.display_update(game_state.screen,
                           active_map.raw_maps,
                           active_map.display_data,
                           game_state.clock)
        update_text = message_font.render(
            "Cities Placed: ...... {0} / {1}".format(
                len(game_state.active_map.cities),
                game_state.active_map.mgp.number_of_cities),
            True,
            util.colors.white)
        game_state.screen.blit(update_text,
                               [10, game_state.screen_height - 24])

        pygame.display.flip()


def set_nation_territory(game_state):
    active_map = game_state.active_map
    print("Debug A")
    claims = {}
    for each_nation in game_state.active_map.nations:
        claims[each_nation] = []
    for each_tile in game_state.active_map.all_tiles:
        if each_tile.is_land():
            closest = (999999, None)
            for each_nation in game_state.active_map.nations:
                cap = each_nation.capital
                d = util.distance(
                    each_tile.column,
                    each_tile.row,
                    cap.column,
                    cap.row)
                if d < closest[0]:
                    closest = (d, each_nation)
            assert closest[1] is not None
            claims[closest[1]].append(each_tile)
    print("Debug B")
    nation.accrete_cities(game_state, claims)
    nation.accrete_city_territory(game_state)
    active_map.set_nation_control()
    active_map.render_raw_maps(['nation'])
    game_state.screen.fill(util.colors.black)
    mgr.display_update(game_state.screen,
                       active_map.raw_maps,
                       active_map.display_data,
                       game_state.clock)

    pygame.display.flip()
    mgr.input_loop(game_state, "Press Enter to Award Unclaimed Tiles.")
    unclaimed_tiles = nation.survey_unclaimed_tiles(game_state)
    nation.award_unclaimed_tiles(game_state, unclaimed_tiles)
    active_map.set_nation_control()
    active_map.render_raw_maps(['nation'])
    game_state.screen.fill(util.colors.black)
    mgr.display_update(game_state.screen,
                       active_map.raw_maps,
                       active_map.display_data,
                       game_state.clock)

    pygame.display.flip()


def make_map(game_state):
    active_map = game_state.active_map
    generate_blank_ocean_tiles(active_map)
    generate_heightmap(active_map)
    adjust_landmass_height(active_map)
    infill_basins(active_map)

    active_map.render_raw_maps(['height'])
    mgr.display_update(game_state.screen,
                       active_map.raw_maps,
                       active_map.display_data,
                       game_state.clock)

    active_map.temperature = generate_tempmap(active_map.width, active_map.height)
    active_map.moisture = generate_moisture_map(
        active_map.width,
        active_map.height,
        active_map.elevation,
        active_map.mgp.water_cutoff)
    set_biomes(active_map, active_map.mgp.water_cutoff)

    generate_rivers(active_map, active_map.mgp.water_cutoff)
    generate_terrain(active_map)
    place_resources(active_map)

    print("Building tile database...")
    for row in active_map.game_tile_rows:
        for tile in row:
            active_map.all_tiles.append(tile)
            prod.set_output(tile)
    print("map complete")

    active_map.render_raw_maps(['height', 'temp', 'moisture', 'water flux', 'biome'])


def map_generation(game_state, active_map: Map):
    mgr.input_loop(game_state)
    mgr.render_map_labels(
        game_state.screen,
        active_map.scaled_maps,
        active_map.display_data)
    mgr.display_update(
        game_state.screen,
        active_map.raw_maps,
        active_map.display_data,
        game_state.clock)
    # generate water, land, rivers, temperature, biomes and resources
    make_map(game_state)
    #
    spawn_cities(game_state)
    nc = game_state.active_map.mgp.number_of_cities
    mgr.input_loop(game_state,
                   "Press Enter to Manifest Destiny.",
                   "Setting Territory for {0} Cities... Please Wait...".format(nc))
    city.set_city_territory(game_state)
    active_map.set_city_control()
    nn = game_state.active_map.mgp.number_of_nations
    mgr.input_loop(
        game_state,
        "Press Enter to Create Nations.",
        "Setting Territory for {0} Nations... Please Wait...".format(nn))
    nation.create_nations(game_state)
    set_nation_territory(game_state)
    months = 120
    mgr.input_loop(
        game_state,
        "Press Enter to Run the Course of History.",
        "Running History for {0} Months... Please Wait...".format(months))
    city.sort_city_tiles(game_state)
    city.run_cities(game_state, months)
    mgr.input_loop(game_state, "Press Enter to accept your fate.")

    # map generation finished

    # prepare map surfaces
    active_map.prepare_surfaces()
    print("Launching")


def load_existing(game_state, vital_records):
    active_map = game_state.active_map
    generate_blank_ocean_tiles(active_map)
    for attr_name in ("moisture", "temperature", "elevation"):
        setattr(active_map, attr_name, vital_records[attr_name])
    for each_record in vital_records["tiles"]:
        column = each_record["column"]
        row = each_record["row"]
        active_map.game_tile_rows[row][column].load_external(each_record)
    for each_record in vital_records["cities"]:
        city_tile = active_map.game_tile_rows[each_record["row"]][each_record["column"]]
        new_city = city.City(
            active_map,
            each_record["column"],
            each_record["row"],
            city_tile,
            each_record["name"])
        new_city.load_external(each_record)
        active_map.add_city(new_city)
    for each_record in vital_records["nations"]:
        new_nation = nation.Nation(active_map)
        new_nation.load_external(each_record)

    print("Building tile database...")
    for row in active_map.game_tile_rows:
        for tile in row:
            active_map.all_tiles.append(tile)
            prod.set_output(tile)
    print("map complete")

    active_map.render_raw_maps(['height', 'temp', 'moisture', 'water flux', 'biome'])

    city.sort_city_tiles(game_state)  # keep
    # map generation finished

    # prepare map surfaces
    active_map.prepare_surfaces()
    print("Launching")
