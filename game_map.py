import pygame
import utilities
from utilities import colors
import queue
import math
import random
import art
from typing import List
import mapgen_render as mgr
import utilities as util
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
        self.number_of_cities = 125
        self.number_of_nations = random.randint(
            math.ceil(map_size / 2),
            math.floor(map_size))
        """Nation Override"""
        self.number_of_nations = 6

    def get_vitals(self):
        vitals = {}
        for attr_name in ("river_cutoff",
                          "water_cutoff",
                          "number_of_clusters",
                          "max_cluster_size",
                          "number_of_cities",
                          "number_of_nations"):
            vitals[attr_name] = getattr(self, attr_name)


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
        self.mgp = MapGenParameters(map_dimensions)
        self.width = map_dimensions[0]
        self.height = map_dimensions[1]
        self.x_shift = 0
        self.y_shift = 0
        self.temperature = []
        self.moisture = []
        self.elevation = []

        self.largest_water_body = None

        self.all_tiles = []
        self.game_tile_rows = []
        self.cities = []
        self.nations = []
        self.agents = set()
        self.player = None

        self.nation_control = []
        self.city_control = []

        for row in range(map_dimensions[1]):
            row = []
            for column in range(map_dimensions[0]):
                row.append(None)
            self.nation_control.append(row)

        for row in range(map_dimensions[1]):
            row = []
            for column in range(map_dimensions[0]):
                row.append(None)
            self.city_control.append(row)

        self.tile_display_layer = None
        self.terrain_display_layer = None
        self.resource_display_layer = None
        self.building_display_layer = None
        self.nation_border_display_layer = None
        self.biome_map_preview = None
        self.raw_maps = self.initialize_raw_maps(self.width, self.height)
        self.scaled_maps = mgr.scale_maps(
            self.raw_maps,
            self.display_data)
        self.screen_dimensions = screen_dimensions

    @property
    def display_data(self):
        return (self.width, self.height, False)

    def serial_prep(self):
        vital_records = {}
        for attr_name in ("moisture", "temperature", "elevation"):
            vital_records[attr_name] = getattr(self, attr_name)
        vital_records["map dimensions"] = (self.width, self.height)
        vital_records["mapgen parameters"] = self.mgp.get_vitals()

        vital_records["tiles"] = []  # List[dict]
        for each_tile in self.all_tiles:
            tile_vitals = each_tile.get_vitals()
            vital_records["tiles"].append(tile_vitals)
        vital_records["cities"] = []  # List[dict]
        for each_city in self.cities:
            city_vitals = each_city.get_vitals()
            vital_records["cities"].append(city_vitals)
        vital_records["nations"] = []  # List[dict]
        for each_nation in self.nations:
            nation_vitals = each_nation.get_vitals()
            vital_records["nations"].append(nation_vitals)
        vital_records["player"] = self.player.get_vitals()
        return vital_records

    def add_city(self, new_city):
        self.cities.append(new_city)

    def set_nation_control(self):
        nc_array = self.nation_control
        for each_nation in self.nations:
            for new_tile in each_nation.tiles:
                nc_array[new_tile.row][new_tile.column] = each_nation
                new_tile.nation = each_nation

    def set_city_control(self):
        cc_array = self.city_control
        for each_city in self.cities:
            for new_tile in each_city.tiles:
                cc_array[new_tile.row][new_tile.column] = each_city
                new_tile.owner = each_city

    def initialize_raw_maps(self, width, height):
        map_previews = [pygame.Surface([width, height])
                        for i in range(8)]
        clean_map_previews = []
        for each in map_previews:
            each.fill((110, 110, 110))
            each.set_colorkey(util.colors.key)
            each = each.convert_alpha()
            clean_map_previews.append(each)
        return clean_map_previews

    def render_raw_maps(self, exclusive=None, viable_sites=None):
        mgr.render_raw_maps(self, exclusive, viable_sites)

    def prepare_surfaces(self):
        self.render_raw_maps()
        self.paint_background_tiles(self.game_tile_rows)
        self.paint_terrain_layer(self.game_tile_rows)
        self.paint_resource_layer(self.game_tile_rows)
        self.paint_building_layer(self.game_tile_rows)
        self.paint_nation_border_layer(self.game_tile_rows)
        scaled_maps = mgr.scale_maps(
            self.raw_maps,
            self.display_data)
        self.biome_map_preview = pygame.Surface([140, 140])
        pygame.transform.smoothscale(scaled_maps[3],
                                     (140, 140),
                                     self.biome_map_preview)
        self.biome_map_preview.set_colorkey(util.colors.key)
        self.biome_map_preview = self.biome_map_preview.convert_alpha()

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

