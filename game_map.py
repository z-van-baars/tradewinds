import pygame
import utilities
from utilities import colors
import queue
import math
import random
import art
from typing import List
assert List

tile_width = 40
tile_height = 15


class MapGenParameters(object):
    def __init__(self, map_dimensions):
        self.river_cutoff = 2000
        self.water_cutoff = 0.5
        self.number_of_clusters = math.floor(
            math.sqrt(map_dimensions[0] * map_dimensions[1]) / 3)
        self.max_cluster_size = 5
        map_size = math.sqrt(math.sqrt(map_dimensions[0] * map_dimensions[1]))
        self.number_of_cities = math.floor(map_size * 5)
        """City Override"""
        self.number_of_cities = 45
        self.number_of_nations = random.randint(
            math.ceil(map_size / 2),
            math.floor(map_size))
        """Nation Override"""
        self.number_of_nations = 4


class DisplayLayer(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        layer_width = (
            (width * math.floor(tile_width / 2)) +
            (height * math.floor(tile_width / 2)))
        layer_height = (
            (width * math.floor(tile_height / 2)) +
            (height * math.floor(tile_height / 2)))
        self.image = pygame.Surface([layer_width, layer_height])
        self.image.fill(colors.key)
        self.rect = self.image.get_rect()


class Map(object):
    def __init__(self, map_dimensions, screen_dimensions):
        self.tile_display_layer = None
        self.terrain_display_layer = None
        self.resource_display_layer = None
        self.building_display_layer = None
        self.nation_border_display_layer = None
        self.screen_dimensions = screen_dimensions
        self.width = map_dimensions[0]
        self.height = map_dimensions[1]
        self.mgp = MapGenParameters(map_dimensions)
        self.game_tile_rows = []
        self.nation_control = []
        for row in range(map_dimensions[1]):
            row = []
            for column in range(map_dimensions[0]):
                row.append(None)
            self.nation_control.append(row)
        self.city_control = []
        for row in range(map_dimensions[1]):
            row = []
            for column in range(map_dimensions[0]):
                row.append(False)
            self.city_control.append(row)

        self.cities = []
        self.nations = []

        self.displayshift_x = 0
        self.displayshift_y = 0
        self.temperature = []
        self.moisture = []
        self.elevation = []
        self.biome_map_preview = None
        self.all_tiles = []
        self.agents = set()

    def add_city(self, new_city):
        self.cities.append(new_city)

    def paint_background_tiles(self, game_tile_rows):
        tile_width = 40
        self.tile_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.tile_display_layer.image.get_width() / 2)
        for y_row in game_tile_rows:
            for tile in y_row:
                new_tile_image = random.choice(art.biome_images[tile.biome])
                x, y = utilities.get_screen_coords(tile.column, tile.row)
                self.tile_display_layer.image.blit(
                    new_tile_image,
                    [x + background_x_middle + (tile_width / 2), y])
        self.tile_display_layer.image.set_colorkey(colors.key)
        self.tile_display_layer.image = self.tile_display_layer.image.convert_alpha()

    def paint_terrain_layer(self, game_tile_rows):
        river_cutoff = self.mgp.river_cutoff
        tile_width = 40
        self.terrain_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.tile_display_layer.image.get_width() / 2)
        for y_row in game_tile_rows:
            for tile in y_row:
                if (tile.terrain and tile.water_flux[2] < river_cutoff and
                        art.terrain_images[tile.terrain][tile.biome]):
                    new_terrain_image = random.choice(
                        art.terrain_images[tile.terrain][tile.biome])
                    x, y = utilities.get_screen_coords(tile.column, tile.row)
                    self.terrain_display_layer.image.blit(
                        new_terrain_image,
                        [x + background_x_middle + (tile_width / 2), y - 25])

                # is this a river?
                if (tile.biome != 'lake' and
                    tile.terrain is not any(["low hill",
                                             "hill",
                                             "low mountain",
                                             "mountain"])):
                    if tile.water_flux[2] > river_cutoff:
                        x, y = utilities.get_screen_coords(tile.column, tile.row)
                        self.terrain_display_layer.image.blit(art.river_images[0],
                                                              [x + background_x_middle +
                                                               (tile_width / 2), y])
                        for source in tile.water_source[0]:
                            self.terrain_display_layer.image.blit(
                                art.river_images[source],
                                [x + background_x_middle +
                                 (tile_width / 2), y])
                        self.terrain_display_layer.image.blit(
                            art.river_images[tile.water_source[1]],
                            [x + background_x_middle +
                             (tile_width / 2), y])

        self.terrain_display_layer.image.set_colorkey(colors.key)
        self.terrain_display_layer.image = (
            self.terrain_display_layer.image.convert_alpha())

    def paint_resource_layer(self, game_tile_rows):
        tile_width = 40
        self.resource_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.resource_display_layer.image.get_width() / 2)
        for y_row in game_tile_rows:
            for tile in y_row:
                if tile.resource:
                    new_resource_image = random.choice(
                        art.resource_images[tile.resource])
                    x, y = utilities.get_screen_coords(tile.column, tile.row)
                    self.resource_display_layer.image.blit(
                        new_resource_image,
                        [x + background_x_middle + (tile_width / 2), y - 25])
        self.resource_display_layer.image.set_colorkey(colors.key)
        self.resource_display_layer.image = (
            self.resource_display_layer.image.convert_alpha())

    def paint_building_layer(self, game_tile_rows):
        tile_width = 40
        self.building_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.building_display_layer.image.get_width() / 2)
        for city in self.cities:
            new_city_image = art.city_1
            x, y = utilities.get_screen_coords(city.column, city.row)
            self.building_display_layer.image.blit(
                new_city_image,
                [x + background_x_middle + (tile_width / 2), y])
        self.building_display_layer.image.set_colorkey(colors.key)
        self.building_display_layer.image = (
            self.building_display_layer.image.convert_alpha())

    def paint_nation_border_layer(self, game_tile_rows):
        tile_width = 40
        self.nation_border_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.building_display_layer.image.get_width() / 2)
        for each_nation in self.nations:
            each_nation.get_border_tiles(self)
            for each_tile in each_nation.border_tiles:
                tile_edge_buffer = pygame.Surface((40, 15))
                tile_edge_buffer.fill(colors.key)
                for key, value in each_tile.bordered_edges.items():
                    if value is True:
                        tile_edge_buffer.blit(art.border_edges[key], [0, 0])

                x, y = utilities.get_screen_coords(each_tile.column, each_tile.row)
                self.nation_border_display_layer.image.blit(
                    tile_edge_buffer,
                    [x + background_x_middle + (tile_width / 2), y])
        self.nation_border_display_layer.image.set_colorkey(colors.key)
        self.nation_border_display_layer.image = (
            self.nation_border_display_layer.image.convert_alpha())

    def world_scroll(self, shift_x, shift_y, screen_width, screen_height):
        background_width = self.tile_display_layer.image.get_width()
        background_height = self.tile_display_layer.image.get_height()
        self.x_shift += shift_x
        self.y_shift += shift_y
        if self.y_shift < -(background_height - 40):
            self.y_shift = -(background_height - 40)
        elif self.y_shift > screen_height + -40:
            self.y_shift = screen_height + -40
        if self.x_shift < -(background_width - 40):
            self.x_shift = -(background_width - 40)
        if self.x_shift > screen_width + -40:
            self.x_shift = screen_width + -40

    def draw_to_screen(self, screen):
        background_x_middle = (
            self.tile_display_layer.rect.left +
            (self.tile_display_layer.image.get_width()) / 2)
        objects_to_draw = queue.PriorityQueue()
        for each in self.constructs:
            screen_coordinates = utilities.get_screen_coords(
                each.tile_x,
                each.tile_y,
                self.x_shift,
                self.y_shift,
                self.tile_display_layer.rect.top,
                background_x_middle)
            objects_to_draw.put((screen_coordinates[1], screen_coordinates[0], each))

        while not objects_to_draw.empty():
            y, x, graphic = objects_to_draw.get()
            screen.blit(graphic.sprite.image, [(x + self.x_shift),
                                               (y + self.y_shift)])

