import utilities as util
import nav
import claim_nav
import production as prod
import math
import random
import numpy as np
from scipy.ndimage import label, generate_binary_structure
import art
import time
from enum import Enum
import pygame


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


class CityFocus(Enum):
    balanced = 0
    growth = 1
    production = 2
    wealth = 3


class City(object):
    def __init__(self, active_map, x, y, tile, name):
        self.active_map = active_map
        self.column = x
        self.row = y
        self.tile = tile
        self.tile.city = self
        self.tiles = []
        self.tiles_sorted = {CityFocus.balanced: [],
                             CityFocus.growth: [],
                             CityFocus.production: [],
                             CityFocus.wealth: []}
        self.ships_available = []
        self.name = name
        self.nation = None
        self.color = (255, 255, 255)
        self.size = 1
        self.focus = CityFocus.balanced
        self.silver = 0
        self.food = 0
        self.demand = {}
        self.supply = {}
        self.sell_price = {}
        self.purchase_price = {}
        self.portrait_img = random.choice(art.city_portraits)
        self.prev_turn_data = TurnData()

        self.set_random_supply()
        self.set_demand_for_artikels()

    def set_random_supply(self):
        for resource in prod.all_artikels:
            self.supply[resource] = 0

    def set_demand_for_artikels(self):
        for artikel_id in prod.all_artikels:
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

    def sort_local_tiles(self):
        for each_tile in self.tiles:
            f = prod.get_food_value(each_tile)
            p = 0
            r = 0
            w = 0
            self.tiles_sorted[CityFocus.balanced].append((f, each_tile))
            self.tiles_sorted[CityFocus.growth].append((f, each_tile))
            self.tiles_sorted[CityFocus.production].append((p, each_tile))
            self.tiles_sorted[CityFocus.wealth].append((r + w, each_tile))
        for each_key, each_value in self.tiles_sorted.items():
            each_value.sort(key=lambda tup: tup[0], reverse=True)

    def collect(self, turn_data):
        # print("collecting...")
        tiles_to_collect = []
        for ii in range(self.size):
            if ii >= len(self.tiles):
                break
            tiles_to_collect.append(self.tiles_sorted[self.focus][ii][1])
        for each_tile in tiles_to_collect:
            # print("new tile")
            # print("{0} {1}".format(each_tile.biome, each_tile.terrain))
            for artikel_id, value in each_tile.output.items():
                if value != 0:
                    self.supply[artikel_id] += value
                    if artikel_id not in turn_data.produced:
                        turn_data.produced[artikel_id] = 0
                    turn_data.produced[artikel_id] += value

    def consume(self, turn_data):
        food_types = ["fish", "fruit", "grain", "meat", "shellfish"]
        for cc in range(self.size):
            fs = turn_data.get_food_stores(self.supply)
            if fs < 5:
                print("starvation!")
                turn_data.starvation += 1
                continue
            for ff in range(5):
                random.shuffle(food_types)
                for artikel_id in food_types:
                    if self.supply[artikel_id] - 1 >= 0:
                        if artikel_id not in turn_data.consumed:
                            turn_data.consumed[artikel_id] = 0
                        turn_data.consumed[artikel_id] += 1
                        self.supply[artikel_id] -= 1
                        break

    def specialist_labor(self, turn_data):
        pass

    def noble_labor(self, turn_data):
        pass

    def set_size(self, turn_data):
        if turn_data.starvation > 0:
            self.size = max(
                1,
                (self.size - min(2, turn_data.starvation)))
            return

        food_types = ["fish", "fruit", "grain", "meat", "shellfish"]
        if turn_data.get_food_stores(self.supply) > turn_data.get_food_box(self.size):
            for ff in range(turn_data.get_food_box(self.size)):
                random.shuffle(food_types)
                for artikel_id in food_types:
                    if self.supply[artikel_id] - 1 >= 0:
                        if artikel_id not in turn_data.consumed:
                            turn_data.consumed[artikel_id] = 0
                        turn_data.consumed[artikel_id] += 1
                        self.supply[artikel_id] -= 1
                        break
            self.size += 1
            print("{0} grew to size {1}".format(self.name, self.size))

    def get_stability(self, turn_data):
        pass

    def get_prices(self, turn_data):
        pass

    def turn_loop(self):
        turn_data = TurnData()
        self.collect(turn_data)
        self.consume(turn_data)
        self.specialist_labor(turn_data)
        self.noble_labor(turn_data)
        turn_data.current_supply = self.supply
        self.set_size(turn_data)
        self.get_stability(turn_data)
        self.get_prices(turn_data)
        self.prev_turn_data = turn_data


class TurnData(object):
    def __init__(self):
        self.starvation = 0
        self.current_supply = {}
        self.produced = {}
        self.consumed = {}

    def get_food_stores(self, supply):
        food_types = ["fish", "fruit", "grain", "meat", "shellfish"]
        fs = 0
        for key, value in supply.items():
            if key in food_types:
                fs += value
        return fs

    def get_food_box(self, size):
        fb = size * 11
        return fb


def find_closest_city(game_state, each_tile, subset=None):
    closest = (999999, None)
    if subset is None:
        subset = game_state.active_map.cities
    for each_city in subset:
        if each_city.tile == each_tile:
            closest = (0, each_city)
            break
        path = claim_nav.get_path(
            [each_tile.row, each_tile.column],
            game_state.active_map,
            [each_city.row, each_city.column])
        if len(path.steps) < closest[0]:
            closest = (len(path.steps), each_city)

    assert closest[1] is not None
    return closest


def set_city_territory(game_state):
    def set_tile_owner(game_state, tile, owner):
        tile.owner = owner
        x1 = tile.column
        y1 = tile.row
        game_state.active_map.city_control[y1][x1] = owner
        if owner is not None:
            owner.tiles.append(tile)
    start = time.time()
    city_claims = {}
    for every_tile in game_state.active_map.all_tiles:
        city_claims[every_tile] = []
    for each_city in game_state.active_map.cities:
        radius_tiles = util.get_nearby_tiles(
            game_state.active_map,
            [each_city.column, each_city.row],
            15)
        for radius_tile in radius_tiles:
            if radius_tile.is_land():
                city_claims[radius_tile].append(each_city)
    for each_tile, claimants in city_claims.items():
        closest = (99999, None)
        if len(claimants) == 1:
            closest = (0, claimants[0])
        elif len(claimants) > 1:
            closest = find_closest_city(game_state, each_tile, claimants)
        set_tile_owner(game_state, each_tile, closest[1])

    end = time.time()
    print("time_elapsed {0}s".format(end - start))


def sort_city_tiles(game_state):
    for each_city in game_state.active_map.cities:
        each_city.sort_local_tiles()


class HistoryCatch(object):
    def __init__(self):
        self.months = {"population": {}}


def run_cities(game_state, months):
    history_catch = HistoryCatch()
    for ii in range(months):
        history_catch.months[ii] = {}
        print("Simulating... {0}".format(game_state.calendar.get_date_string()))
        for each_city in game_state.active_map.cities:
            each_city.turn_loop()
            if each_city.nation not in history_catch.months[ii]:
                history_catch.months[ii][each_city.nation] = 0
            history_catch.months[ii][each_city.nation] += each_city.size
        game_state.calendar.next_month()

    marker = pygame.Surface([1, 1])
    marker.fill(util.colors.light_green)
    graph_buffer = pygame.Surface(
        [game_state.screen.get_width(), game_state.screen.get_height()])
    graph_buffer.fill(util.colors.black)
    for month, nation_dict in history_catch.months.items():
        for each_nation, pop in nation_dict.items():
            marker.fill(each_nation.color)
            graph_buffer.blit(
                marker,
                [month, game_state.screen.get_height() - pop / 5])
    print("rendered")
    graph = True
    while graph:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    graph = False
        game_state.screen.blit(graph_buffer, [0, 0])
        game_state.clock.tick(60)

        pygame.display.flip()


def evaluate_local_food(active_map, zone_of_control):
    total_local_food = 0
    for each in zone_of_control:
        total_local_food += (
            prod.food_value[each.biome] + prod.terrain_food_value[each.terrain])
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


def add_new_city(active_map, candidate):
    name_chosen = False
    while not name_chosen:
        new_name = random.choice(city_names)
        if not any((city.name == new_name) for city in active_map.cities):
            name_chosen = True
    new_city = City(active_map, candidate.column, candidate.row, candidate, new_name)
    active_map.cities.append(new_city)
    candidate.city = new_city

