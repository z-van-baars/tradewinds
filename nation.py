import utilities as util
import art
import random


nation_names = []
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
lines = nn.readlines()
for line in lines:
    line = line.capitalize()
    nation_names.append(line[:-1])
nn.close()


class Nation(object):
    def __init__(self, active_map, number, color):
        self.name = random.choice(nation_names)
        self.color = color
        self.active_map = active_map
        self.number = number
        self.cities = []
        self.tiles = []


    def growth_turn(self):
        for each_city in self.cities:
            each_city.turn_loop()


grow_nations(game_state):
    active_map = game_state.active_map
    nations = active_map.nations

    while game_state.calendar.year < 100:
        for each_nation in nations:
            each_nation.growth_turn()

        game_state.calendar.increment_date(2)

