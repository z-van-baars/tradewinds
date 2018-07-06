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

    for subarray in layers:
        print(np.sum(subarray))

    sorted_water_bodies = sorted(((np.sum(subarray), subarray) for subarray in layers), key=lambda x: x[0], reverse=True)
    for size, water_body in sorted_water_bodies:
        print(size)
    largest_water_body = sorted_water_bodies[0][1]
    return largest_water_body


def evaluate_distance_to_cities(cities, tile):
    total_distance_score = 0
    for each in cities:
        distance = util.distance(tile.column, tile.row, each.column, each.row)
        distance = max(0, 6 - distance)
        total_distance_score += distance * 20
    return math.floor(total_distance_score)


def evaluate_total_score(zone_of_control, food_score, temperature_score, resource_score, tile, existing_cities):
    distance_score = evaluate_distance_to_cities(existing_cities, tile)
    city_score = len(zone_of_control) + food_score + temperature_score + resource_score * 15 - distance_score
    time.sleep(0)
    return city_score


def get_zone_of_control(active_map, tile):
    zone_of_control = util.get_nearby_tiles(active_map, (tile.column, tile.row), 4)
    return zone_of_control


def add_new_city(active_map, city_candidates, zone_of_control, food_score, temperature_score, resource_score, cities):
    city_sites = queue.PriorityQueue()
    for each in city_candidates:
        city_score = evaluate_total_score(zone_of_control[each.row][each.column],
                                          food_score[each.row][each.column],
                                          temperature_score[each.row][each.column],
                                          resource_score[each.row][each.column],
                                          each,
                                          cities)
        if city_score > 0:
            city_sites.put((-city_score, each))
            active_map.city_score[each.row][each.column] = city_score
        else:
            active_map.city_score[each.row][each.column] = 0

    score, candidate = city_sites.get()
    name_chosen = False
    while not name_chosen:
        new_name = random.choice(city_names)
        if not any((city.name == new_name) for city in active_map.cities):
            name_chosen = True
    print(new_name)
    new_city = City(candidate.column, candidate.row, new_name)
    cities.append(new_city)
    candidate.city = new_city
    active_map.city_score[candidate.row][candidate.column] = 0
    city_candidates.remove(candidate)
    return cities


def cull_non_coastal_tiles(city_candidates, active_map):
    print("culling non coastal tiles...")

    coastal_tiles = []
    for each_tile in city_candidates:
        neighbor_tiles = util.get_adjacent_tiles(each_tile, active_map)
        if any(neighbor.biome in ['ocean', 'sea', 'shallows'] for neighbor in neighbor_tiles):
            coastal_tiles.append(each_tile)

    connected_coastal_tiles = []
    largest_water_body = cull_interior_watermasses(active_map)
    print(largest_water_body)
    for each in coastal_tiles:
        neighbor_tiles = util.get_adjacent_tiles(each, active_map)
        if any(largest_water_body[neighbor.column, neighbor.row] == 1 for neighbor in neighbor_tiles):
            connected_coastal_tiles.append(each)
        else:
            print("dropped an interior coastline tile")

    return connected_coastal_tiles


def survey_city_sites(active_map):
    city_candidates = []
    for y in active_map.game_tile_rows:
        for x in y:
            if x.biome != "ocean" and x.biome != "ice" and x.biome != "sea" and x.biome != "shallows":
                if x.terrain != "mountain" and x.terrain != "low_mountain" and x.terrain != "hill":
                    city_candidates.append(x)

    city_candidates = cull_non_coastal_tiles(city_candidates, active_map)
    food_score = []
    temperature_score = []
    zone_of_control = []
    city_score = []
    resource_score = []

    for y in range(active_map.height):
        row = []
        row2 = []
        row3 = []
        row4 = []
        row5 = []
        for x in range(active_map.width):
            row.append(None)
            row2.append([])
            row3.append(0)
            row4.append(0)
            row5.append(0)
        food_score.append(row)
        temperature_score.append(row5)
        zone_of_control.append(row2)
        resource_score.append(row3)
        city_score.append(row4)
        active_map.city_score = city_score

    for each in city_candidates:
        zone_of_control[each.row][each.column] = get_zone_of_control(active_map, each)
        food_score[each.row][each.column] = evaluate_local_food(active_map, zone_of_control[each.row][each.column])
        temperature_score[each.row][each.column] = math.floor(active_map.temperature[each.row][each.column] / 3)
        resource_score[each.row][each.column] = evaluate_local_resources(active_map, zone_of_control[each.row][each.column])
        z = (len(zone_of_control[each.row][each.column]))
        f = food_score[each.row][each.column]
        t = temperature_score[each.row][each.column]
        r = resource_score[each.row][each.column] * 15
        d = 0
        active_map.city_score[each.row][each.column] = z + f + t + r - d

    return zone_of_control, food_score, temperature_score, resource_score, city_score, city_candidates
