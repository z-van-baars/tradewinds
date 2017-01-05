import random
import utilities
import spice


port_coordinates = {"London": (1305, 245),
                    "Cardiff": (1281, 248),
                    "Dublin": (1265, 237),
                    "Belfast": (1271, 221),
                    "Edinburgh": (1291, 215),
                    "Constantinople": (1496, 340),
                    "Rome": (1394, 336),
                    "Naples": (1407, 345),
                    "Venice": (1390, 301),
                    "Alexandria": (1523, 423),
                    "Barcelona": (1319, 335),
                    "Valencia": (1300, 350),
                    "Porto": (1243, 331),
                    "Lisbon": (1236, 361),
                    "Marseille": (1340, 320),
                    "Bordeaux": (1296, 304),
                    "Amsterdam": (1340, 237),
                    "Rotterdam": (1332, 250),
                    "Copenhagen": (1384, 217),
                    "Athens": (1467, 368),
                    "Jerusalem": (1557, 410),
                    "Tunis": (1373, 374),
                    "Tangier": (1257, 386),
                    "Dakar": (1166, 561),
                    "Porto Novo": (1319, 638),
                    "Cape Town": (1435, 990),
                    "Maputo": (1540, 919),
                    "Zanzibar": (1593, 748),
                    "Bombay": (1845, 527),
                    "Calicut": (1869, 591),
                    "Madras": (1903, 585),
                    "Calcutta": (1960, 500),
                    "Canton": (2148, 495),
                    "Hong Kong": (2153, 500),
                    "Shanghai": (2183, 429),
                    "Tianjin": (2134, 357),
                    "Bangkok": (0, 0),
                    "Taipei": (0, 0),
                    "Singapore": (0, 0),
                    "Jakarta": (0, 0),
                    "Busan": (0, 0)}


def get_demand():
    demand = utilities.roll_dice(3, 40)
    if random.randint(1, 100) < 5:
        demand += utilities.roll_dice(3, 40)
    demand *= 0.1
    return demand


class Port(object):
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
        self.parent_node = None
        self.demand = {}
        self.supply = {}
        self.sell_price = {}
        self.purchase_price = {}
        self.distance_to = {}

    def set_supply(self):
        pass

    def set_random_supply(self):
        for each in spice.spices:
            self.supply[each] = random.randint(0, 100)

    def set_demand_for_spices(self):
        for each in spice.spices:
            self.demand[each] = get_demand()
            self.sell_price[each] = round(self.demand[each] * spice.base_cost[each] * 0.8)
            self.purchase_price[each] = round(self.demand[each] * spice.base_cost[each] * 1.1)

    def calculate_distances(self, ports):
        for each in ports:
            self.distance_to[each] = utilities.distance(self.x, self.y, ports[each].x, ports[each].y)




