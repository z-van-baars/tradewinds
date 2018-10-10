import utilities as util
import queue
import math
import random
import artikel
import numpy as np
from scipy.ndimage import label, generate_binary_structure
import time


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
              "ocean": 2,
              "sea": 2,
              "shallows": 2,
              "lake": 1,
              "river": 1}

terrain_food_value = {"vegetation": 1.0,
                      "low hill": 0.8,
                      "hill": 0.6,
                      "low mountain": 0.4,
                      "mountain": 0.25}


movement_cost = {"taiga": 1,
                 "tundra": 2,
                 "snowy tundra": 2,
                 "grassland": 1,
                 "plains": 1,
                 "wet plains": 2,
                 "savannah": 1,
                 "desert": 2,
                 "forest": 2,
                 "jungle": 2,
                 "snowpack": 2,
                 "ice": 2,
                 "shrubland": 1,
                 "ocean": 1,
                 "sea": 0.5,
                 "shallows": 0.5,
                 "lake": 0.5,
                 "river": 0.3}


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
        self.size = 0
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
            self.sell_price[artikel_id] = round(
                self.demand[artikel_id] * base_price * 0.8)
            self.purchase_price[artikel_id] = round(
                self.demand[artikel_id] * base_price * 1.1)

    def increment_supply(self, artikel_id, quantity):
        if artikel_id in self.supply:
            self.supply[artikel_id] += quantity
        else:
            self.supply[artikel_id] = quantity


def evaluate_local_food(active_map, zone_of_control):
    # local_tiles = utilities.get_nearby_tiles(active_map, (tile.column, tile.row), 3)
    total_local_food = 0
    for each in zone_of_control:
        total_local_food += (
            food_value[each.biome] * terrain_food_value[each.terrain])
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

    trade_score = (site.tile.water_flux[2] ** (1.0 / 3.0)) * 3
    trade_score = min(trade_score, 55)
    if site in coastal_sites:
        trade_score *= 1.25
        trade_score += 10
    return trade_score


def math_helper(z, f, t, r, tr, d):
    """Algorithms"""
    return z + f + t + r * 20 + ((tr / 2) * (tr / 2)) - d


def evaluate_city_score(active_map, site):
    zoc = site.zone_of_control
    z = (len(zoc))
    f = site.food_score
    t = site.temperature_score
    tr = site.trade_score
    r = site.resource_score
    d = site.distance_score
    # as the map fills up, we want to weight proximity to other cities less and less
    # crowding_factor = ((active_map.number_of_cities - len(active_map.cities)) / active_map.number_of_cities)
    return max(50, math_helper(z, f, t, r, tr, d))


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


class Site(object):
    def __init__(self, tile, active_map):
        self.tile = tile
        self.establish_initial_scores(active_map)

    def establish_initial_scores(self, active_map):
        self.zone_of_control = get_zone_of_control(active_map, self.tile)
        self.food_score = evaluate_local_food(active_map, self.zone_of_control)
        self.temperature_score = math.floor(active_map.temperature[self.tile.row][self.tile.column] / 3)
        self.resource_score = evaluate_local_resources(active_map, self.zone_of_control)
        self.distance_score = get_distance_score(active_map, self.tile)
        self.trade_score = 0
        self.city_score = 0

    def update_scores(self, active_map, coastal_sites):
        self.distance_score = get_distance_score(active_map, self.tile)
        self.trade_score = get_trade_score(active_map, coastal_sites, self)
        self.city_score = evaluate_city_score(active_map, self)

    def is_viable(self):
        return (
            self.tile.biome != "ocean" and
            self.tile.biome != "ice" and
            self.tile.biome != "sea" and
            self.tile.biome != "shallows" and
            self.tile.biome != "lake" and
            self.tile.terrain != "mountain" and
            self.tile.terrain != "low_mountain" and
            self.tile.terrain != "hill")


def add_new_city(active_map, viable_sites, coastal_sites):
    city_sites = queue.PriorityQueue()
    for site in viable_sites:
        if site.city_score > 1:
            city_sites.put((-site.city_score, site.tile, site))
    score, candidate, site = city_sites.get()
    name_chosen = False
    while not name_chosen:
        new_name = random.choice(city_names)
        if not any((city.name == new_name) for city in active_map.cities):
            name_chosen = True
    print(new_name)
    new_city = City(candidate.column, candidate.row, new_name)
    active_map.cities.append(new_city)
    candidate.city = new_city
    site.city_score = 50
    viable_sites.remove(site)
