import pygame
import math
import random
import pickle
import numpy as np


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.display.set_caption("Tradewinds v 0.1")


months = ["January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"]

month_days = {"January": 31,
              "February": 28,
              "March": 31,
              "April": 30,
              "May": 31,
              "June": 30,
              "July": 31,
              "August": 31,
              "September": 30,
              "October": 31,
              "November": 30,
              "December": 31}


class Calendar(object):
    def __init__(self):
        self.year = 1
        self.month = 0
        self.day = 1
        self.month_string = months[self.month]

    def increment_date(self):
        self.day += 1

        if self.day > month_days[self.month_string]:
            self.month += 1
            self.day = 1
        if self.month > 11:
            self.year += 1
            self.month = 0
        self.month_string = months[self.month]

    def get_date_string(self):
        return "{0} {1}, {2}".format(self.month_string, self.day, self.year)


class Colors(object):
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.background_blue = (16, 69, 87)
        self.light_gray = (194, 194, 194)
        self.light_green = (0, 210, 0)
        self.yellow = (239, 210, 19)
        self.dark_green = (0, 200, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.bright_blue = (8, 248, 252)
        self.blue_grey = (180, 210, 217)
        self.purple = (255, 0, 255)
        self.key = (255, 0, 128)
        self.brown = (112, 87, 46)
        self.dragbar = (36, 92, 104)
        self.biome_colors = {
            "ocean": (0, 0, 255),
            "sea": (25, 25, 255),
            "shallows": (50, 50, 255),
            "ice": (255, 255, 255),
            "snowpack": (255, 255, 255),
            "tundra": (8, 248, 252),
            "snowy tundra": (8, 248, 252),
            "taiga": (88, 224, 119),
            "grassland": (0, 210, 0),
            "jungle": (77, 142, 61),
            "forest": (29, 71, 19),
            "shrubland": (90, 70, 46),
            "snowpack": (225, 225, 255),
            "plains": (112, 87, 46),
            "wet plains": (112, 87, 46),
            "desert": (244, 240, 70),
            "savannah": (244, 167, 66),
            "river": (255, 255, 255),
            "lake": (50, 50, 255)}
        self.nation_colors = [
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


colors = Colors()


class Path(object):
    def __init__(self):
        self.steps = []

    def get_step(self):
        step = self.steps.pop(0)
        return step


def on_screen(screen_width, screen_height, x_position, y_position, x_shift, y_shift):
    if 0 <= x_position + x_shift <= screen_width and 0 <= y_position + y_shift <= screen_height - 80:
        return True
    else:
        return False


def any_tile_visible(screen_width, screen_height, x_shift, y_shift, entity):
    initial_x = entity.tile_x
    initial_y = entity.tile_y - (entity.footprint[1] - 1)
    for tile_y in range(initial_y, initial_y + (entity.footprint[1])):
        for tile_x in range(initial_x, initial_x + entity.footprint[0]):
            if on_screen(screen_width, screen_height, tile_x * 20, tile_y * 20, x_shift, y_shift):
                return True
    return False


def get_random_coordinates(x_lower, x_upper, y_lower, y_upper):
        x_position = random.randint(x_lower, x_upper)
        y_position = random.randint(y_lower, y_upper)
        return (x_position, y_position)


def any_tile_blocked(tile, active_map, entity):
    initial_x = tile.column
    initial_y = tile.row - (entity.footprint[1] - 1)
    for tile_y in range(initial_y, initial_y + (entity.footprint[1])):
        for tile_x in range(initial_x, initial_x + entity.footprint[0]):
            if within_map(tile_x, tile_y, active_map):
                if active_map.game_tile_rows[tile_y][tile_x].is_occupied():
                    return True
            else:
                return True
    return False


def distance(a, b, x, y):
    a1 = abs(a - x)
    b1 = abs(b - y)
    c = math.sqrt((a1 * a1) + (b1 * b1))
    return c


def quit_check():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()


# function for N repeated rolls of random(S+1), returning a number from 0 to N*S
def roll_dice(number_of_dice, sides):
    # Sum of N dice each of which goes from 0 to sides
    value = 0
    for i in range(number_of_dice):
        value += random.randint(1, sides)
    return value


def get_nearby_tiles(current_map, center, radius):
    # includes center tile
    nearby_tiles = []
    x = center[0]
    y = center[1]
    for tile_y in range((y - radius), (y + radius)):
        for tile_x in range((x - radius), (x + radius)):
            if within_map(tile_x, tile_y, current_map.game_tile_rows):
                distance_from_center = math.ceil(
                    distance(tile_x, tile_y, center[0], center[1]))
                if distance_from_center < radius:
                    nearby_tiles.append(current_map.game_tile_rows[tile_y][tile_x])
    return nearby_tiles


def within_map(x, y, current_map):
    return 0 <= x <= len(current_map[0]) - 1 and 0 <= y <= len(current_map) - 1


def get_adjacent_tiles(tile, current_map):
    # excludes center tile
    initial_x = tile.column - 1
    initial_y = tile.row - 1
    adjacent_tiles = []
    for tile_y in range(initial_y, initial_y + 3):
        for tile_x in range(initial_x, initial_x + 3):
            if within_map(tile_x, tile_y, current_map.game_tile_rows):
                adjacent_tiles.append(current_map.game_tile_rows[tile_y][tile_x])
    adjacent_tiles.remove(tile)
    return adjacent_tiles


def get_fat_x(tile, active_map):
    # excludes center tile
    adjacent_tiles = get_adjacent_tiles(tile, active_map)
    outer_ring_xy = [(-1, -2), (0, -2), (1, -2),
                     (-2, -1), (-2, 0), (-2, 1),
                     (2, -1), (2, 0), (2, 1),
                     (-1, 2), (0, 2), (1, 2)]
    outer_ring = []
    for xy_pair in outer_ring_xy:
        if within_map(tile.column + xy_pair[0], tile.row + xy_pair[1], active_map.game_tile_rows):
            new_tile = active_map.game_tile_rows[tile.row + xy_pair[1]][tile.column + xy_pair[0]]
            outer_ring.append(new_tile)
    return outer_ring + adjacent_tiles


def get_adjacent_movement_tiles(tile, current_map):
    # includes center tile
    initial_x = tile.column - 1
    initial_y = tile.row - 1
    adjacent_tiles = []
    for tile_y in range(initial_y, initial_y + 3):
        for tile_x in range(initial_x, initial_x + 3):
            if within_map(tile_x, tile_y, current_map.game_tile_rows):
                adjacent_tiles.append(current_map.game_tile_rows[tile_y][tile_x])
    return adjacent_tiles


def check_if_inside(x1, x2, y1, y2, pos):
    return x1 < pos[0] < x2 and y1 < pos[1] < y2


def get_vector(self, a, b, x, y):
    distance_to_target = distance(a, b, x, y)
    factor = distance_to_target / self.speed
    x_dist = a - x
    y_dist = b - y
    change_x = x_dist / factor
    change_y = y_dist / factor

    return (change_x, change_y)


def get_neighbor_position(tile, neighbor):
    slots = {(-1, -1): 1,
             (0, -1): 2,
             (1, -1): 3,
             (1, 0): 4,
             (1, 1): 5,
             (0, 1): 6,
             (-1, 1): 7,
             (-1, 0): 8}

    x_dif = neighbor.column - tile.column
    y_dif = neighbor.row - tile.row

    diff = (x_dif, y_dif)
    neighbor_slot = slots[diff]

    return neighbor_slot


def get_map_coords(pos, x_shift, y_shift, background_x_middle):
    x_true = (pos[0] - x_shift) - (background_x_middle - x_shift)
    y_true = pos[1] - y_shift
    x = int((x_true / 20 + y_true / 7) / 2)
    y = int((y_true / 7 - x_true / 20) / 2)
    return (x, y)


def get_screen_coords(x_tile, y_tile):
    x = int((((x_tile + 1) - (y_tile + 1)) * 20) - 20)
    y = int(((y_tile + x_tile) * 7))
    return (x, y)


def sigmoid(x):
    return 1 / (1 + math.exp(-x))
