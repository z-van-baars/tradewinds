import utilities as util
import queue
import nav
import production as prod
import math
import random
import artikel
import numpy as np
from scipy.ndimage import label, generate_binary_structure
import art


city_names = []

cn = open('city_names.txt', 'r')
lines = cn.readlines()
for line in lines:
    line = line.capitalize()
    city_names.append(line[:-1])
cn.close()


def get_demand():
    demand = util.roll_dice(3, 40)
    if random.randint(1, 100) < 5:
        demand += util.roll_dice(3, 40)
    demand *= 0.1
    return demand


class City(object):
    def __init__(self, active_map, x, y, tile, name):
        self.active_map = active_map
        self.column = x
        self.row = y
        self.tile = tile
        self.name = name
        self.size = 0
        self.province_tiles = []
        self.workers = set()
        self.demand = {}
        self.supply = {}
        self.sell_price = {}
        self.purchase_price = {}
        self.province_border = []
        self.portrait_img = random.choice(art.city_portraits)

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

    def grow(self):
        pass

    def harvest_resources(self, active_map):
        for worker in self.workers:
            resources_gathered = worker.work_tile()
            for key, value in resources_gathered.items():
                self.supply[key] += value

    def produce_secondary_goods(self):
        pass

    def turn_loop(self, active_map):
        self.harvest_resources(active_map)
        self.produce_secondary_goods()
        self.grow()

    def get_province_border(self, active_map):
        province_border = []
        border_tiles = []
        frontier = set()
        neighbors = util.get_adjacent_tiles(self.tile, active_map)
        for each in neighbors:
            if each in self.province_tiles:
                frontier.add(each)
        visited = set()
        while len(frontier) > 0:
            new_tile = frontier.pop()
            if new_tile not in visited:
                visited.add(new_tile)
                tile_neighbors = util.get_adjacent_tiles(new_tile, active_map)
                for each in tile_neighbors:
                    if each in self.province_tiles and each not in visited:
                        frontier.add(each)
                if any(each not in self.province_tiles for each in tile_neighbors):
                    if new_tile not in border_tiles:
                        border_tiles.append(new_tile)
        print(len(border_tiles))

        for each_tile in border_tiles:
            xy_pair = util.get_screen_coords(each_tile.column, each_tile.row)
            province_border.append(xy_pair)

        self.province_border = province_border


def evaluate_local_food(active_map, zone_of_control):
    # local_tiles = utilities.get_nearby_tiles(active_map, (tile.column, tile.row), 3)
    total_local_food = 0
    for each in zone_of_control:
        total_local_food += (
            prod.food_value[each.biome] * prod.terrain_food_value[each.terrain])
    return total_local_food


def evaluate_local_resources(active_map, zone_of_control):
    # local_tiles = utilities.get_nearby_tiles(active_map, (tile.column, tile.row), 3)
    total_local_resources = 0
    for each in zone_of_control:
        if each.resource:
            total_local_resources += 1
    return total_local_resources


def get_movement_cost(active_map, tile):
    cost = nav.movement_cost[tile.biome] * nav.terrain_movement_cost[tile.terrain]
    return cost


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


def math_helper(z, f, t, r, tr):
    """Algorithms"""
    return z + f + t + r * 20 + ((tr / 2) * (tr / 2))


def evaluate_city_score(active_map, site):
    zoc = site.zone_of_control
    z = (len(zoc))
    f = site.food_score
    t = site.temperature_score
    tr = site.trade_score
    r = site.resource_score

    return max(50, math_helper(z, f, t, r, tr))


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

    sorted_water_bodies = sorted(
        ((np.sum(subarray), subarray) for subarray in layers),
        key=lambda x: x[0], reverse=True)
    largest_water_body = sorted_water_bodies[0][1]
    return largest_water_body


class Site(object):
    def __init__(self, tile, active_map):
        self.active_map = active_map
        self.tile = tile
        self.establish_initial_scores(active_map)

    def establish_initial_scores(self, active_map):
        self.zone_of_control = get_zone_of_control(active_map, self.tile)
        self.food_score = evaluate_local_food(active_map, self.zone_of_control)
        self.temperature_score = math.floor(
            active_map.temperature[self.tile.row][self.tile.column] / 3)
        self.resource_score = evaluate_local_resources(active_map, self.zone_of_control)
        self.trade_score = 0
        self.city_score = 0

    def update_scores(self, active_map, coastal_sites):
        self.trade_score = get_trade_score(active_map, coastal_sites, self)
        self.city_score = evaluate_city_score(active_map, self)

    def is_viable(self):
        return self.tile.biome not in ("ocean", "ice", "sea",
                                       "shallows", "lake", "mountain",
                                       "low_mountain", "hill")

    def lock_neighborhood(self, active_map, viable_sites):
        neighborhood = util.get_fat_x(self.tile, active_map)
        print("removing fat x from the running")
        for i, tile in enumerate(neighborhood, start=1):
            for site in viable_sites:
                if site.tile == tile:
                    site.city_score = 20
                    viable_sites.remove(site)
                    break
        print("removed {0} tiles from the running".format(i))


def add_new_city(active_map, sorted_sites, viable_sites):
    score, candidate, site = sorted_sites.get()

    name_chosen = False
    while not name_chosen:
        new_name = random.choice(city_names)
        if not any((city.name == new_name) for city in active_map.cities):
            name_chosen = True
    print("Debug C")
    print(new_name)
    new_city = City(active_map, candidate.column, candidate.row, candidate, new_name)
    active_map.cities.append(new_city)
    candidate.city = new_city
    site.city_score = 20
    site.lock_neighborhood(active_map, viable_sites)
