import utilities
import queue
import time
import math

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
                 "lake": 1,
                 "river": 1}


terrain_movement_cost = {"mountain": 5.0,
                         "low mountain": 3.0,
                         "hill": 2.0,
                         "low hill": 1.5,
                         "vegetation": 1}


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


def evaluate_connectivity(active_map, evaluated_coast_tiles, tile):
    print("evaluating...")

    def evaluate_frontier_tile(frontier_tile, edge_tiles):
        neighbors = utilities.get_adjacent_tiles(frontier_tile, active_map)
        for each in neighbors:
            if each.biome == "ocean" and each not in connected_ocean_tiles:
                connected_ocean_tiles.append(each)
                frontier.put(each)
            elif each.biome != "ocean" and each not in edge_tiles:
                edge_tiles.append(each)

    ocean_size_threshold = (active_map.width * active_map.height) * 0.10

    frontier = queue.PriorityQueue()
    frontier.put(tile)
    edge_tiles = []
    connected_ocean_tiles = []
    while not frontier.empty():
        frontier_tile = frontier.get()
        evaluate_frontier_tile(frontier_tile, edge_tiles)
        print(len(connected_ocean_tiles))

    if len(connected_ocean_tiles) > ocean_size_threshold:
        for each in edge_tiles:
            evaluated_coast_tiles[each] = True
        return True, evaluated_coast_tiles
    for each in edge_tiles:
        evaluated_coast_tiles[each] = False
    return False, evaluated_coast_tiles


def get_zone_of_control_old(active_map, tile):
    frontier = queue.PriorityQueue()
    frontier.put((get_movement_cost(active_map, tile), tile))
    max_move_cost = 5
    zone_of_control = []
    while not frontier.empty():

        cost_so_far, new_tile = frontier.get()
        if new_tile not in zone_of_control:
            zone_of_control.append(new_tile)
            neighbors = utilities.get_adjacent_tiles(new_tile, active_map)
            for each in neighbors:
                if get_movement_cost(active_map, each) + cost_so_far < max_move_cost and each not in zone_of_control:
                    frontier.put((cost_so_far + get_movement_cost(active_map, each), each))
    return zone_of_control


def get_zone_of_control(active_map, tile):
    zone_of_control = utilities.get_nearby_tiles(active_map, (tile.column, tile.row), 4)
    return zone_of_control


def evaluate_distance_to_cities(cities, tile):
    total_distance_score = 0
    for each in cities:
        distance = utilities.distance(tile.column, tile.row, each.column, each.row)
        distance = max(0, 6 - distance)
        total_distance_score += distance * 20
    return math.floor(total_distance_score)


def evaluate_total_score(zone_of_control, food_score, temperature_score, resource_score, tile, existing_cities):
    distance_score = evaluate_distance_to_cities(existing_cities, tile)
    city_score = len(zone_of_control) + food_score + temperature_score + resource_score * 15 - distance_score
    # print("City Score: {0} / Zone of Control {1} / Food Score {2} / Resource Score {3} / Distance Score {4}".format(city_score, len(zone_of_control), food_score, resource_score, distance_score))
    # print(len(zone_of_control), local_food, city_score)
    # print("city_scored...")
    time.sleep(0)
    return city_score


def add_new_city(active_map, city_candidates, zone_of_control, food_score, temperature_score, resource_score, cities):
    city_sites = queue.PriorityQueue()
    print(len(city_candidates))
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

    print("debug C")
    score, candidate = city_sites.get()
    cities.append(candidate)
    active_map.city_score[candidate.row][candidate.column] = 0
    city_candidates.remove(candidate)
    return cities


def cull_non_coastal_tiles(city_candidates, active_map):
    print("culling non coastal tiles...")
    coastal_tiles = []
    for each_tile in city_candidates:
        neighbor_tiles = utilities.get_adjacent_tiles(each_tile, active_map)
        if any(neighbor.biome == "ocean" for neighbor in neighbor_tiles):
            coastal_tiles.append(each_tile)
    connected_coastal_tiles = []
    evaluated_coastal_tiles = {}
    for each in coastal_tiles:
        print("{0} of {1}...".format(coastal_tiles.index(each) + 1, len(coastal_tiles)))
        if each not in evaluated_coastal_tiles:
            evaluated_coastal_tiles[each], evaluated_coastal_tiles = evaluate_connectivity(active_map,
                                                                                           evaluated_coastal_tiles,
                                                                                           each)
    for each in coastal_tiles:
        if evaluated_coastal_tiles[each]:
            connected_coastal_tiles.append(each)
    print("non coastal tiles culled!")
    return connected_coastal_tiles


def survey_city_sites(active_map):
    city_candidates = []
    for y in active_map.game_tile_rows:
        for x in y:
            if x.biome != "ocean" and x.biome != "ice":
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
