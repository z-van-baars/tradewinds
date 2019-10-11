import random
import math
import utilities
import queue


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
                 "lake": 0.5}


terrain_movement_cost = {"mountain": 5.0,
                         "low mountain": 3.0,
                         "hill": 2.0,
                         "low hill": 1.5,
                         "vegetation": 1,
                         "river": 1}



def distance(a, b, x, y):
    a1 = abs(a - x)
    b1 = abs(b - y)
    c = math.sqrt((a1 * a1) + (b1 * b1))
    return c


def calculate_step(my_position, next_tile):
    x_dist = my_position[0] - next_tile.column
    y_dist = my_position[1] - next_tile.row
    if abs(x_dist) > abs(y_dist):
        if x_dist < 0:
            change_x = 1
        elif x_dist > 0:
            change_x = -1
        change_y = 0
    elif abs(x_dist) < abs(y_dist):
        if y_dist < 0:
            change_y = 1
        elif y_dist > 0:
            change_y = -1
        change_x = 0
    else:
        if y_dist < 0:
            change_y = 1
        elif y_dist > 0:
            change_y = -1
        if x_dist < 0:
            change_x = 1
        elif x_dist > 0:
            change_x = -1
    return change_x, change_y


def explore_frontier_to_target(game_map, visited, target_tile, closest_tile, frontier):
    while not frontier.empty():
        priority, current_tile, previous_tile = frontier.get()
        new_steps = visited[previous_tile][0] + 1
        if current_tile not in visited or new_steps < visited[current_tile][0]:
            tile_neighbors = utilities.get_adjacent_tiles(current_tile, game_map)
            for each in tile_neighbors:
                if each == target_tile or not each.is_occupied():
                    if each.terrain == "river" or each.biome in ("ocean",
                                                                 "sea",
                                                                 "shallows",
                                                                 "lake"):
                        distance_to_target = distance(each.column,
                                                      each.row,
                                                      target_tile.column,
                                                      target_tile.row)
                        priority = distance_to_target + new_steps
                        frontier.put((priority, each, current_tile))
            distance_to_target = distance(current_tile.column,
                                          current_tile.row,
                                          target_tile.column,
                                          target_tile.row)
            if distance_to_target < closest_tile[0]:
                closest_tile = [distance_to_target, current_tile]
            visited[current_tile] = (new_steps, previous_tile)
        if target_tile in visited:
            break
    return closest_tile


def get_path(my_position, game_map, target_coordinates):
    target_tile = game_map.game_tile_rows[target_coordinates[1]][target_coordinates[0]]
    start_tile = game_map.game_tile_rows[my_position[1]][my_position[0]]
    visited = {start_tile: (0, None)}
    tile_neighbors = utilities.get_adjacent_tiles(start_tile, game_map)
    frontier = queue.PriorityQueue()
    closest_tile = [99999, start_tile]
    for each in tile_neighbors:
        if not each.is_occupied() and (each.terrain == "river" or
                                       each.biome in ("ocean",
                                                      "sea",
                                                      "shallows",
                                                      "lake")):
            frontier.put((0, each, start_tile))
    closest_tile = explore_frontier_to_target(
        game_map,
        visited,
        target_tile,
        closest_tile,
        frontier)

    if closest_tile[1] is not target_tile:
        print("no target_match!")
        return None

    new_path = utilities.Path()
    new_path.steps = [closest_tile[1]]
    while True:
        next_tile = new_path.steps[0]
        if visited[next_tile][1] == start_tile:
            break
        new_path.steps.insert(0, visited[next_tile][1])
    return new_path

