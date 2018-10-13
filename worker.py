import production as prod
import utilities as util
import math


class Worker(object):
    def __init__(self, active_map, city):
        self.active_map = active_map
        self.home_city = city
        self.tile = None

    def work_tile(self):
        resource_output = {}
        d = math.floor(util.distance(
            self.tile.column, self.tile.row,
            self.home_city.column, self.home_city.row))
        for key, value in prod.chart[self.tile.biome]:
            # reduce output by 10% per tile distant from main city, max output reduction 90%
            # add pathing check to see if there's a road to and from the tile, reduce by only 5%, max reduction still 90%
            resource_output[key] = value * min(1 - d * 0.1, 0.1)
        return resource_output

