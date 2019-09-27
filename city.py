import utilities as util
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


def get_city_name(cities_list):
    name_chosen = False
    while not name_chosen:
        new_name = random.choice(city_names)
        if not any((city.name == new_name) for city in cities_list):
            name_chosen = True
    return new_name


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
        self.tile.city = self
        self.tiles = []
        self.ships_available = []
        self.name = name
        self.nation = None
        self.color = (255, 255, 255)
        self.size = 1
        self.silver = 0
        self.food = 0
        self.demand = {}
        self.supply = {}
        self.sell_price = {}
        self.purchase_price = {}
        self.portrait_img = random.choice(art.city_portraits)
        self.settlers = 0

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
        growth_cap = 10
        g = random.randint(1, 100)
        if self.food <= growth_cap:
            return
        if g > 33:
            self.size += 1
            self.food -= 10
            print("A city has grown!")
            print("{0} is now size {1}".format(self.name, self.size))
            return
        print("A settler is spawned")
        self.size -= 1
        self.food -= 10
        self.settlers += 1

    def allocate_workers(self, active_map):
        tiles_to_work = []
        local_tiles = []
        for each in util.get_fat_x(self.tile, active_map):
            f = (prod.food_value[each.biome] * prod.terrain_food_value[each.terrain])
            r = 0
            if each.resource:
                r = 1
            w = prod.wealth_value[each.biome] * prod.terrain_wealth_value[each.terrain]
            score = r + f + w
            local_tiles.append((score, each, r, f, w))
        if len(local_tiles) < 1:
            print(self.name)
            print((self.column, self.row))
            print(len(util.get_fat_x(self.tile, active_map)))
        local_tiles.sort()
        local_tiles.reverse()

        w = 1
        while len(local_tiles) > 0:
            tiles_to_work.append(local_tiles.pop())
        surplus_workers = w - self.size

        return tiles_to_work, surplus_workers

    def eat(self):
        food_needed = self.size * 1
        if self.food < food_needed:
            print("starvation!")
            self.size = max(self.size - 1, 1)
            self.food = 0
        else:
            self.food -= food_needed

    def work_tiles(self, tiles_to_work):
        for each_tile in tiles_to_work:
            self.food += each_tile[3]
            self.silver += each_tile[4]

    def harvest_resources(self, active_map):
        for worker in self.workers:
            resources_gathered = worker.work_tile()
            for key, value in resources_gathered.items():
                self.supply[key] += value

    def produce_secondary_goods(self):
        pass

    def turn_loop(self, active_map):
        tiles_to_work, surplus_workers = self.allocate_workers(active_map)
        self.work_tiles(tiles_to_work)
        self.eat()
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


def get_distance_score(active_map, site):
    "Penalize city sites by their proximity to other cities squared"
    map_size = math.sqrt(
        math.sqrt(active_map.width *
                  active_map.height))
    d = 0
    for each_city in active_map.cities:
        dist = util.distance(site.tile.column,
                             site.tile.row,
                             each_city.column,
                             each_city.row)
        d += max(0,
                 (-map_size + (max(0, (map_size - dist)) ** 2)))
        d *= 2
    return d


def math_helper(z, f, t, r, tr, d):
    """Algorithms"""
    return -d + z + f + t + r * 20 + tr + ((tr / 2) * (tr / 2))


def evaluate_city_score(active_map, site):
    zoc = site.zone_of_control
    z = (len(zoc))
    f = site.food_score
    t = site.temperature_score
    tr = site.trade_score
    r = site.resource_score
    d = site.distance_score

    return max(50, math_helper(z, f, t, r, tr, d))


def cull_interior_watermasses(active_map):
    water_array = np.ones((active_map.width, active_map.height))
    for row in active_map.game_tile_rows:
        for tile in row:
            if tile.biome not in ["ocean", "sea", "shallows"]:
                water_array[tile.column, tile.row] = 0
    s = generate_binary_structure(2, 2)
    labeled_array, num_features = label(water_array, structure=s)
    print("Large Water Bodies: {0}".format(num_features))

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

    def __lt__(self, other):
        return False

    def establish_initial_scores(self, active_map):
        self.zone_of_control = get_zone_of_control(active_map, self.tile)
        self.food_score = evaluate_local_food(active_map, self.zone_of_control)
        self.temperature_score = math.floor(
            active_map.temperature[self.tile.row][self.tile.column] / 3)
        self.resource_score = evaluate_local_resources(active_map, self.zone_of_control)
        self.distance_score = get_distance_score(active_map, self)
        self.trade_score = 0
        self.city_score = 0

    def update_scores(self, active_map, coastal_sites):
        self.distance_score = get_distance_score(active_map, self)
        self.trade_score = get_trade_score(active_map, coastal_sites, self)
        self.city_score = evaluate_city_score(active_map, self)

    def is_viable(self):
        return self.tile.biome not in ("ocean", "ice", "sea",
                                       "shallows", "lake", "mountain",
                                       "low_mountain", "hill")

    def lock_neighborhood(self, active_map, viable_sites):
        neighborhood = util.get_fat_x(self.tile, active_map)
        for i, tile in enumerate(neighborhood, start=1):
            for site in viable_sites:
                if site.tile == tile:
                    site.city_score = 20
                    viable_sites.remove(site)
                    break
        # print("removed {0} tiles from the running".format(i))


def add_new_city(active_map, candidate):
    name_chosen = False
    while not name_chosen:
        new_name = random.choice(city_names)
        if not any((city.name == new_name) for city in active_map.cities):
            name_chosen = True
    new_city = City(active_map, candidate.column, candidate.row, candidate, new_name)
    active_map.cities.append(new_city)
    candidate.city = new_city

