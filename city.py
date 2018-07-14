import utilities as util
import queue
import time
import math
import random
import artikel
import numpy as np
import pygame
from scipy.ndimage import label, generate_binary_structure


city_names = []

cn = open('city_names.txt', 'r')
lines = cn.readlines()
for line in lines:
    city_names.append(line[:-1])
cn.close()

food_value = {"taiga": 2,
              "tundra": 1,
              "snowy tundra": 1,
              "grassland": 3,
              "plains": 2,
              "wet plains": 2,
              "savannah": 1,
              "desert": 0,
              "forest": 2,
              "jungle": 2,
              "snowpack": 0,
              "ice": 0,
              "shrubland": 1,
              "ocean": 1,
              "sea": 1,
              "shallows": 1,
              "lake": 1,
              "river": 1}

terrain_food_value = {"vegetation": 1.0,
                      "low hill": 0.8,
                      "hill": 0.6,
                      "low mountain": 0.4,
                      "mountain": 0.25}


movement_cost = {"taiga": 1,
                 "tundra": 2,
                 "snowy tundra": 3,
                 "grassland": 1,
                 "plains": 1,
                 "wet plains": 2,
                 "savannah": 1,
                 "desert": 3,
                 "forest": 3,
                 "jungle": 3,
                 "snowpack": 3,
                 "ice": 3,
                 "shrubland": 2,
                 "ocean": 1,
                 "sea": 1,
                 "shallows": 1,
                 "lake": 1,
                 "river": 1}


terrain_movement_cost = {"mountain": 5.0,
                         "low mountain": 3.0,
                         "hill": 2.0,
                         "low hill": 1.5,
                         "vegetation": 1}


def get_demand():
    demand = util.roll_dice(3, 40)
    if random.randint(1, 100) < 5:
        demand += util.roll_dice(3, 40)
    demand *= 0.1
    return demand


class City(object):
    def __init__(self, x, y, name):
        self.column = x
        self.row = y
        self.name = name
        self.demand = {}
        self.supply = {}
        self.produces = {}
        self.industries = []
        self.sell_price = {}
        self.purchase_price = {}

        self.set_random_supply()
        self.set_demand_for_artikels()

    def set_random_supply(self):
        for resource in artikel.all_resources:
            self.supply[resource] = random.randint(0, 100)

    def set_demand_for_artikels(self):
        for artikel_id in artikel.all_resources:
            base_price = 100
            self.demand[artikel_id] = get_demand()
            self.sell_price[artikel_id] = round(self.demand[artikel_id] * base_price * 0.8)
            self.purchase_price[artikel_id] = round(self.demand[artikel_id] * base_price * 1.1)

    def increment_supply(self, artikel_id, quantity):
        if artikel_id in self.supply:
            self.supply[artikel_id] += quantity
        else:
            self.supply[artikel_id] = quantity


def evaluate_local_food(active_map, zone_of_control):
    # local_tiles = utilities.get_nearby_tiles(active_map, (tile.column, tile.row), 3)
    total_local_food = 0
    for each in zone_of_control:
        total_local_food += food_value[each.biome] * terrain_food_value[each.terrain]
    return total_local_food


def evaluate_local_resources(active_map, zone_of_control):
    # local_tiles = utilities.get_nearby_tiles(active_map, (tile.column, tile.row), 3)
    total_local_resources = 0
    for each in zone_of_control:
        if each.resource:
            total_local_resources += 1
    return total_local_resources


def get_movement_cost(active_map, tile):
    cost = movement_cost[tile.biome] * terrain_movement_cost[tile.terrain]
    return cost


def get_distance_score(active_map, tile):
    total_distance_score = 0
    for each in active_map.cities:
        distance = util.distance(tile.column, tile.row, each.column, each.row)
        power = 3  # * (len(active_map.cities) / active_map.number_of_cities)
        map_size = math.sqrt(active_map.width * active_map.height)
        distance = max(0, ((0.16 * map_size) - distance)) ** power
        total_distance_score += distance * 0.1  # / len(active_map.cities)
    return math.floor(total_distance_score)


def get_zone_of_control(active_map, tile):
    zone_of_control = util.get_nearby_tiles(active_map, (tile.column, tile.row), 4)
    return zone_of_control


def get_trade_score(active_map, coastal_sites, site):
    trade_score = 0

    trade_score = (site.water_flux[2] ** (1.0 / 3.0)) * 3
    trade_score = min(trade_score, 55)
    if site in coastal_sites:
        trade_score *= 1.25
        trade_score + 40

    return trade_score


def evaluate_city_score(active_map, scores, site):
    zoc = scores['zone of control'][site]
    z = (len(zoc))
    f = scores['food score'][site]
    t = scores['temperature score'][site]
    tr = scores['trade score'][site]
    r = scores['resource score'][site]
    d = scores['distance score'][site]
    # as the map fills up, we want to weight proximity to other cities less and less
    crowding_factor = ((active_map.number_of_cities - len(active_map.cities)) / active_map.number_of_cities)
    city_score = z + f * 2 + t + r * 20 + ((tr / 2) * (tr / 2)) - d
    city_score = max(50, city_score)
    time.sleep(0)
    return city_score


def cull_interior_watermasses(active_map):
    water_array = np.ones((active_map.width, active_map.height))
    for row in active_map.game_tile_rows:
        for tile in row:
            if tile.biome not in ["ocean", "sea", "shallows"]:
                water_array[tile.column, tile.row] = 0
    s = generate_binary_structure(2, 2)
    labeled_array, num_features = label(water_array, structure=s)
    print("water bodies: {0}".format(num_features))

    # filter the labeled array into layers. `==` does the filtering
    layers = [(labeled_array == i) for i in range(1, num_features + 1)]

    sorted_water_bodies = sorted(((np.sum(subarray), subarray) for subarray in layers), key=lambda x: x[0], reverse=True)
    largest_water_body = sorted_water_bodies[0][1]
    return largest_water_body


def cull_non_coastal_tiles(active_map, viable_sites):
    print("culling non coastal tiles...")

    coastal_tiles = []
    for each_tile in viable_sites:
        neighbor_tiles = util.get_adjacent_tiles(each_tile, active_map)
        if any(neighbor.biome in ['ocean', 'sea', 'shallows'] for neighbor in neighbor_tiles):
            coastal_tiles.append(each_tile)

    connected_coastal_tiles = []
    largest_water_body = cull_interior_watermasses(active_map)
    for each in coastal_tiles:
        neighbor_tiles = util.get_adjacent_tiles(each, active_map)
        if any(largest_water_body[neighbor.column, neighbor.row] == 1 for neighbor in neighbor_tiles):
            connected_coastal_tiles.append(each)

    return connected_coastal_tiles


def get_viable_sites(active_map):
    viable_sites = []
    for y in active_map.game_tile_rows:
        for x in y:
            if x.biome != "ocean" and x.biome != "ice" and x.biome != "sea" and x.biome != "shallows" and x.biome != "lake":
                if x.terrain != "mountain" and x.terrain != "low_mountain" and x.terrain != "hill":
                    viable_sites.append(x)
    return viable_sites


def initialize_blank_scores(active_map):
    scores = {'distance score': {},
              'zone of control': {},
              'trade score': {},
              'food score': {},
              'temperature score': {},
              'trade score': {},
              'resource score': {},
              'city score': {}}

    for score_type in ['distance score',
                       'zone of control',
                       'trade score',
                       'food score',
                       'temperature score',
                       'trade score',
                       'resource score',
                       'city score']:
        for y in range(active_map.height):
            for x in range(active_map.width):
                scores[score_type][active_map.game_tile_rows[y - 1][x - 1]] = 0
    return scores


def survey_city_sites(active_map, viable_sites, coastal_sites, scores, initial=False):
    print("surveying sites...")
    for each in viable_sites:
        if initial:
            scores['zone of control'][each] = get_zone_of_control(active_map, each)
            zoc = scores['zone of control'][each]
            scores['food score'][each] = evaluate_local_food(active_map, zoc)
            scores['temperature score'][each] = math.floor(active_map.temperature[each.row][each.column] / 3)
            scores['resource score'][each] = evaluate_local_resources(active_map, zoc)

        scores['distance score'][each] = get_distance_score(active_map, each)
        scores['trade score'][each] = get_trade_score(active_map, coastal_sites, each)
        scores['city score'][each] = evaluate_city_score(active_map, scores, each)
    return scores


def add_new_city(active_map, viable_sites, coastal_sites, scores):
    city_sites = queue.PriorityQueue()
    for site in viable_sites:
        if scores['city score'][site] > 1:
            city_sites.put((-scores['city score'][site], site))

    score, candidate = city_sites.get()
    name_chosen = False
    while not name_chosen:
        new_name = random.choice(city_names)
        if not any((city.name == new_name) for city in active_map.cities):
            name_chosen = True
    print(new_name)
    new_city = City(candidate.column, candidate.row, new_name)
    active_map.cities.append(new_city)
    candidate.city = new_city
    scores['city score'][candidate] = 50
    viable_sites.remove(candidate)
    scores = survey_city_sites(active_map, viable_sites, coastal_sites, scores)
