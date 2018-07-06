import random
import math
import utilities
import queue


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
                    if each.biome == "ocean":
                        distance_to_target = distance(each.column, each.row, target_tile.column, target_tile.row)
                        priority = distance_to_target + new_steps
                        frontier.put((priority, each, current_tile))
            distance_to_target = distance(current_tile.column, current_tile.row, target_tile.column, target_tile.row)
            if distance_to_target < closest_tile[0]:
                closest_tile = [distance_to_target, current_tile]
            visited[current_tile] = (new_steps, previous_tile)
        if target_tile in visited:
            break
    return visited, closest_tile


def get_path(my_position, game_map, target_coordinates):
    target_tile = game_map.game_tile_rows[target_coordinates[1]][target_coordinates[0]]
    start_tile = game_map.game_tile_rows[my_position[1]][my_position[0]]
    visited = {start_tile: (0, None)}
    tile_neighbors = utilities.get_adjacent_tiles(start_tile, game_map)
    frontier = queue.PriorityQueue()
    closest_tile = [99999, start_tile]
    for each in tile_neighbors:
        if not each.is_occupied() and each.biome == "ocean":
            frontier.put((0, each, start_tile))
    visited, closest_tile = explore_frontier_to_target(game_map, visited, target_tile, closest_tile, frontier)

    new_path = utilities.Path()
    new_path.tiles.append(closest_tile[1])
    new_path.steps.append(visited[closest_tile[1]][1])
    while start_tile not in new_path.tiles:
        next_tile = new_path.steps[-1]
        if next_tile != start_tile:
            new_path.steps.append(visited[next_tile][1])
        new_path.tiles.append(next_tile)
    new_path.tiles.reverse()
    # removes the start tile from the tiles list and the steps list in the path object
    new_path.tiles.pop(0)
    new_path.steps.reverse()
    new_path.steps.pop(0)
    return new_path, (closest_tile[1].column, closest_tile[1].row)

