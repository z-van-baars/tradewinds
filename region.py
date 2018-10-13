import math
import queue
import utilities as util
import city

water_biomes = ['ocean',
                'sea',
                'shallows',
                'river']


def find_closest_city(active_map, tile):
    closest_city = (9999, None)
    for each_city in active_map.cities:
        d = util.distance(tile.column, tile.row, each_city.column, each_city.row)
        if d < closest_city[0]:
            closest_city = (d, each_city)
    return closest_city[1]


def assign_provinces(active_map):
    print("assigning provinces...")
    for tile in active_map.all_tiles:
        util.quit_check()
        closest_city = find_closest_city(active_map, tile)
        tile.closest_city = closest_city
        closest_city.province_tiles.append(tile)

    print("drawing borders...")
    for each_city in active_map.cities:
        each_city.get_province_border(active_map)


def grow_cities(active_map):
    print("growing cities...")
    for each_city in active_map.cities:
        zoc = city.get_zone_of_control(active_map, each_city)
        food_score = city.evaluate_local_food(active_map, zoc)
        each_city.size = food_score


def choose_capitals(active_map):
    map_size = math.sqrt(math.sqrt(math.sqrt(active_map.width, active_map.height)))
    number_of_regions = round(len(active_map.cities) / map_size)
    for region in number_of_regions:
        capital = None
        print(capital)


def carve_regions(active_map, capitals):
    all_tiles = active_map.all_tiles
    for tile in all_tiles:
        capitals_by_distance = []
        for each_city in capitals:
            path_cost = get_path(
                (tile.column, tile.row), active_map, (each_city.column, each_city.row))
            capitals_by_distance.append((path_cost, each_city))
        capitals_sorted = sorted(capitals_by_distance)
        print(capitals_sorted)


def get_tile_movement_cost(active_map, previous_tile, current_tile):
    if previous_tile.biome in water_biomes and current_tile.biome not in water_biomes:
        current_tile_cost = 10
    elif previous_tile.biome not in water_biomes and current_tile.biome in water_biomes:
        current_tile_cost = 10
    elif previous_tile.water_flux[2] >= (
        active_map.river_cutoff and (
            current_tile.water_flux[2] < active_map.river_cutoff)):
        current_tile_cost = 10
    elif previous_tile.water_flux[2] < (
        active_map.river_cutoff and (
            current_tile.water_flux[2] >= active_map.river_cutoff)):
        current_tile_cost = 10
    elif previous_tile.water_flux[2] >= (
        active_map.river_cutoff and (
            current_tile.water_flux[2] >= active_map.river_cutoff)):
        current_tile_cost = 0.4 * city.get_movement_cost(active_map, current_tile)
    else:
        current_tile_cost = city.get_movement_cost(active_map, current_tile)
    return current_tile_cost


def explore_frontier_to_target(active_map, visited, target_tile, closest_tile, frontier):
    while not frontier.empty():
        priority, current_tile, previous_tile = frontier.get()

        current_tile_cost = get_tile_movement_cost(
            active_map, previous_tile, current_tile)
        new_steps = visited[previous_tile][0] + current_tile_cost
        if current_tile not in visited or new_steps < visited[current_tile][0]:
            tile_neighbors = util.get_adjacent_tiles(current_tile, active_map)
            for each in tile_neighbors:
                if each == target_tile or not each.is_occupied():
                    distance_to_target = util.distance(
                        each.column, each.row, target_tile.column, target_tile.row)
                    priority = distance_to_target + new_steps
                    frontier.put((priority, each, current_tile))
            distance_to_target = util.distance(
                current_tile.column, current_tile.row,
                target_tile.column, target_tile.row)
            if distance_to_target < closest_tile[0]:
                closest_tile = [distance_to_target, current_tile]
            visited[current_tile] = (new_steps, previous_tile)
        if target_tile in visited:
            break
    return visited, closest_tile


def get_path(my_position, active_map, target_coordinates):
    target_tile = active_map.game_tile_rows[target_coordinates[1]][target_coordinates[0]]
    start_tile = active_map.game_tile_rows[my_position[1]][my_position[0]]
    visited = {start_tile: (0, None)}
    tile_neighbors = util.get_adjacent_tiles(start_tile, active_map)
    frontier = queue.PriorityQueue()
    closest_tile = [99999, start_tile]
    for each in tile_neighbors:
        if not each.is_occupied() and each.biome == "ocean":
            frontier.put((0, each, start_tile))
    visited, closest_tile = explore_frontier_to_target(
        active_map, visited, target_tile, closest_tile, frontier)

    new_path = util.Path()
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




