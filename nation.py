import utilities as util
import art
import city
import random


nation_colors = [
    (128, 0, 0),
    (154, 99, 36),
    (128, 128, 128),
    (0, 128, 128),
    (0, 0, 128),
    (230, 25, 75),
    (245, 25, 75),
    (245, 130, 48),
    (255, 255, 25),
    (210, 245, 60),
    (60, 180, 75),
    (70, 240, 240),
    (0, 130, 200),
    (145, 30, 180),
    (240, 50, 230),
    (250, 190, 190),
    (255, 215, 180),
    (255, 250, 200),
    (170, 255, 195)]

nn = open('nation_names.txt', 'r')
nation_names = []
lines = nn.readlines()
for line in lines:
    line = line.capitalize()
    nation_names.append(line[:-1])
nn.close()


def get_nation_name(nations_list):
    name_chosen = False
    while not name_chosen:
        new_name = random.choice(nation_names)
        if not any((each_nation.name == new_name) for each_nation in nations_list):
            name_chosen = True
    return new_name


class Nation(object):
    def __init__(self, active_map, number, color, name):
        self.name = name
        self.color = color
        self.active_map = active_map
        self.number = number
        self.cities = []
        self.tiles = []

    def add_city(self, new_city):
        self.cities.append(new_city)
        neighborhood = util.get_nearby_tiles(
            self.active_map,
            (new_city.column, new_city.row),
            6)
        for each_tile in neighborhood:
            self.active_map.national_control[each_tile.row][each_tile.column] = self
            self.tiles.append(each_tile)
            each_tile.nation = self

    def mapgen_turn(self):
        for each_city in self.cities:
            each_city.turn_loop(self.active_map)
        total_settlers = 0
        for each_city in self.cities:
            total_settlers += each_city.settlers
            each_city.settlers = 0
        if total_settlers > 0:
            for settler in range(total_settlers):
                unclaimed_tiles = self.get_unclaimed_tiles()
                sorted_frontier = self.sort_unclaimed_tiles(unclaimed_tiles)
                if len(sorted_frontier) < 1:
                    print("no accessible sites to grow to")
                    return
                self.settle_new_city(sorted_frontier)

    def get_tiles_near_cities(self):
        nearby_tiles = []
        nearby_unclaimed_tiles = []
        for each_city in self.cities:
            tiles_in_radius = util.get_nearby_tiles(
                self.active_map,
                (each_city.column, each_city.row),
                8)
            land_tiles = list(filter(lambda x: x.biome not in [
                'ocean',
                'sea',
                'shallows',
                'lake',
                'ice'], tiles_in_radius))
            settleable_tiles = list(filter(lambda x: x.terrain not in [
                'mountain',
                'low mountain',
                'hill'], land_tiles))
            nearby_tiles.extend(settleable_tiles)
        for each_tile in nearby_tiles:
            if each_tile.nation is None:
                nearby_unclaimed_tiles.append(each_tile)
        return nearby_unclaimed_tiles

    def cull_claimed_tiles(self, nearby_tiles):
        print("culling claimed tiles...")
        claimed_tiles = []
        unclaimed_tiles = []
        for each_nation in self.active_map.nations:
            claimed_tiles.extend(each_nation.tiles)
        for tile in nearby_tiles:
            if tile not in claimed_tiles:
                unclaimed_tiles.append(tile)
        return unclaimed_tiles

    def get_unclaimed_tiles(self):
        print("getting nearby unclaimed frontier tiles...")
        unclaimed_tiles = self.get_tiles_near_cities()
        return unclaimed_tiles

    def sort_unclaimed_tiles(self, unclaimed_tiles):
        def is_coastal(active_map, largest_water_body, tile):
            neighbor_tiles = util.get_adjacent_tiles(tile, active_map)
            return (any(neighbor.biome in (
                ['ocean', 'sea', 'shallows']) for neighbor in neighbor_tiles) and
                any(largest_water_body[neighbor.column, neighbor.row] == 1
                    for neighbor in neighbor_tiles))
        print("sorting unclaimed tiles...")
        tiles_to_sort = []
        largest_water_body = city.cull_interior_watermasses(self.active_map)
        coastal_sites = list(filter(lambda x: is_coastal(self.active_map,
                                                         largest_water_body,
                                                         x), unclaimed_tiles))
        for each_tile in unclaimed_tiles:
            new_site = city.Site(each_tile, self.active_map)
            new_site.update_scores(self.active_map, coastal_sites)
            tiles_to_sort.append((new_site.city_score, new_site.tile))
        tiles_to_sort.sort()
        tiles_to_sort.reverse()
        return tiles_to_sort

    def settle_new_city(self, sorted_frontier):
        print("yetahk")
        score, tile = sorted_frontier.pop()
        new_city_name = city.get_city_name(self.active_map.cities)
        print("yabadoo")
        new_city = city.City(
            self.active_map,
            tile.column,
            tile.row,
            tile,
            new_city_name)
        print("yendar")
        self.add_city(new_city)
        self.active_map.add_city(new_city)




