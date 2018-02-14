import pygame
import art
import utilities
import random

# Make constructs remember their choice for multiple choice sprites


class Construct(object):
    display_name = "N/A"
    radius = 0

    def __init__(self, x, y, active_map):
        self.active_map = active_map
        self.tile_x = x
        self.tile_y = y
        self.sprite = pygame.sprite.Sprite()
        self.orbit = []

    def __lt__(self, other):
        return False

    def set_image(self):
        self.sprite.rect = self.sprite.image.get_rect()


class City(Construct):
    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()

    def set_image(self):
        self.sprite.image = art.city_image_1
        self.sprite.image = self.sprite.image.convert_alpha()


class Forest(Construct):
    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()

    def set_image(self):
        self.sprite.image = art.tree_image_1
        self.sprite.image = self.sprite.image.convert_alpha()
