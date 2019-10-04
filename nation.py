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


def get_nation_color(nations_list):
    color_chosen = False
    while not color_chosen:
        new_color = random.choice(util.colors.nation_colors)
        if not any((each_nation.color == new_color) for each_nation in nations_list):
            color_chosen = True
    return new_color


class Nation(object):
    def __init__(self, active_map):
        self.active_map = active_map
        self.name = get_nation_name(active_map.nations)
        self.color = get_nation_color(active_map.nations)

        self.capital = None  # City()
        self.cities = []  # List[City()]
        self.tiles = []  # List[GameTile()]
        self.border_tiles = []  # List[GameTile()]

    def get_border_tiles(self, active_map):
        for each_tile in self.tiles:
            each_tile.bordered_edges = util.get_bordered_edges(
                active_map,
                each_tile)
            if any(each_tile.bordered_edges.values()):
                self.border_tiles.append(each_tile)

    def get_vitals(self):
        vitals = {}
        for attr_name in ("name",
                          "color"):
            vitals[attr_name] = getattr(self, attr_name)
        vitals["capital"] = (self.capital.column, self.capital.row)
        vitals["cities"] = []
        for each_city in self.cities:
            vitals["cities"].append((each_city.column, each_city.row))
        vitals["tiles"] = []
        for each_tile in self.tiles:
            vitals["tiles"].append((each_tile.column, each_tile.row))
        return vitals

    def load_external(self, records):
        for attr_name in ("name",
                          "color"):
            setattr(self, attr_name, records[attr_name])
        (column, row) = records["capital"]
        self.capital = (
            self.active_map.game_tile_rows[row][column].city)
        for each_xy in records["cities"]:
            (column, row) = each_xy
            each_city = self.active_map.game_tile_rows[row][column].city
            self.cities.append(each_city)
        for each_xy in records["tiles"]:
            (column, row) = each_xy
            each_tile = self.active_map.game_tile_rows[row][column]
            self.tiles.append(each_tile)
        self.get_border_tiles(self.active_map)


def get_capital_cities(game_state):
    capital_cities = []
    for n in range(game_state.active_map.mgp.number_of_nations):
        capital_cities.append(game_state.active_map.cities[n])
    return capital_cities


def create_nations(game_state):
    capital_cities = get_capital_cities(game_state)

    for capital in capital_cities:
        new_nation = Nation(game_state.active_map)
        new_nation.capital = capital
        game_state.active_map.nations.append(new_nation)


def accrete_cities(game_state, claims):
    print(len(game_state.active_map.nations))
    for each_nation in game_state.active_map.nations:
        for each_tile in claims[each_nation]:
            if each_tile.city is not None:
                each_nation.cities.append(each_tile.city)
                each_tile.city.nation = each_nation


def accrete_city_territory(game_state):
    for each_nation in game_state.active_map.nations:
        for new_city in each_nation.cities:
            each_nation.tiles = each_nation.tiles + new_city.tiles


def survey_unclaimed_tiles(game_state):
    unclaimed_tiles = []
    for each_tile in game_state.active_map.all_tiles:
        if each_tile.is_land() and each_tile.nation is None:
            unclaimed_tiles.append(each_tile)
    return unclaimed_tiles


def award_unclaimed_tiles(game_state, unclaimed_tiles):
    nc_array = game_state.active_map.nation_control
    for unclaimed_tile in unclaimed_tiles:
        nearby_claims = {}
        for each_nation in game_state.active_map.nations:
            nearby_claims[each_nation] = 0
        best_claimant = (0, None)
        search_radius = 15
        while best_claimant[1] is None:
            claim_neighborhood = util.get_nearby_tiles(
                game_state.active_map,
                [unclaimed_tile.column, unclaimed_tile.row],
                search_radius)

            for nearby_tile in claim_neighborhood:
                if nearby_tile.nation is not None:
                    nearby_claims[nearby_tile.nation] += 1
            for claimant, claim_count in nearby_claims.items():
                if claim_count > best_claimant[0]:
                    best_claimant = (claim_count, claimant)
            search_radius += 5
        assert best_claimant[1] is not None
        unclaimed_tile.nation = best_claimant[1]
        best_claimant[1].tiles.append(unclaimed_tile)
        nc_array[unclaimed_tile.row][unclaimed_tile.column] = best_claimant[1]



