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


class DisplayLayer(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        layer_width = (width * math.floor(tile_width / 2)) + (height * math.floor(tile_width / 2))
        layer_height = (width * math.floor(tile_height / 2)) + (height * math.floor(tile_height / 2))
        self.image = pygame.Surface([layer_width, layer_height])
        self.image.fill(colors.key)
        self.rect = self.image.get_rect()


class Map(object):
    def __init__(self, map_dimensions, screen_dimensions):
        self.tile_display_layer = None
        self.terrain_display_layer = None
        self.resource_display_layer = None
        self.building_display_layer = None
        self.screen_dimensions = screen_dimensions
        self.width = map_dimensions[0]
        self.height = map_dimensions[1]
        self.game_tile_rows = []
        self.number_of_cities = 50
        self.cities = []
        self.river_cutoff = 2000
        self.water_cutoff = 0.5
        self.max_resource_cluster_size = 5
        self.displayshift_x = 0
        self.displayshift_y = 0
        self.temperature = []
        self.moisture = []
        self.elevation = []
        self.biome_map_preview = None
        self.all_tiles = []

    def paint_background_tiles(self, game_tile_rows):
        tile_width = 40
        self.tile_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.tile_display_layer.image.get_width() / 2)
        for y_row in game_tile_rows:
            for tile in y_row:
                new_tile_image = random.choice(art.biome_images[tile.biome])
                x, y = utilities.get_screen_coords(tile.column, tile.row)
                self.tile_display_layer.image.blit(new_tile_image, [x + background_x_middle + (tile_width / 2), y])
        self.tile_display_layer.image.set_colorkey(colors.key)
        self.tile_display_layer.image = self.tile_display_layer.image.convert_alpha()

    def paint_terrain_layer(self, game_tile_rows):
        river_cutoff = self.river_cutoff
        tile_width = 40
        self.terrain_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.tile_display_layer.image.get_width() / 2)
        for y_row in game_tile_rows:
            for tile in y_row:
                if tile.terrain and tile.water_flux[2] < river_cutoff and art.terrain_images[tile.terrain][tile.biome]:
                    new_terrain_image = random.choice(art.terrain_images[tile.terrain][tile.biome])
                    x, y = utilities.get_screen_coords(tile.column, tile.row)
                    self.terrain_display_layer.image.blit(new_terrain_image, [x + background_x_middle + (tile_width / 2), y - 25])

                if tile.biome != 'lake' and tile.terrain is not any(["low hill", "hill", "low mountain", "mountain"]):
                    if tile.water_flux[2] > river_cutoff:
                        x, y = utilities.get_screen_coords(tile.column, tile.row)
                        self.terrain_display_layer.image.blit(art.river_images[0], [x + background_x_middle + (tile_width / 2), y])
                        for source in tile.water_source[0]:
                            self.terrain_display_layer.image.blit(art.river_images[source],
                                                                  [x + background_x_middle + (tile_width / 2), y])
                        self.terrain_display_layer.image.blit(art.river_images[tile.water_source[1]],
                                                              [x + background_x_middle + (tile_width / 2), y])

        self.terrain_display_layer.image.set_colorkey(colors.key)
        self.terrain_display_layer.image = self.terrain_display_layer.image.convert_alpha()

    def paint_resource_layer(self, game_tile_rows):
        tile_width = 40
        self.resource_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.resource_display_layer.image.get_width() / 2)
        for y_row in game_tile_rows:
            for tile in y_row:
                if tile.resource:
                    new_resource_image = random.choice(art.resource_images[tile.resource])
                    x, y = utilities.get_screen_coords(tile.column, tile.row)
                    self.resource_display_layer.image.blit(new_resource_image, [x + background_x_middle + (tile_width / 2), y - 25])
        self.resource_display_layer.image.set_colorkey(colors.key)
        self.resource_display_layer.image = self.resource_display_layer.image.convert_alpha()

    def paint_building_layer(self, game_tile_rows):
        tile_width = 40
        self.building_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.building_display_layer.image.get_width() / 2)
        for city in self.cities:
            new_city_image = art.city_1
            x, y = utilities.get_screen_coords(city.column, city.row)
            self.building_display_layer.image.blit(new_city_image, [x + background_x_middle + (tile_width / 2), y])
        self.building_display_layer.image.set_colorkey(colors.key)
        self.building_display_layer.image = self.building_display_layer.image.convert_alpha()

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
        background_x_middle = self.tile_display_layer.rect.left + (self.tile_display_layer.image.get_width()) / 2
        objects_to_draw = queue.PriorityQueue()
        for each in self.constructs:
            screen_coordinates = utilities.get_screen_coords(each.tile_x,
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

