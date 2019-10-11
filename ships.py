import nav
import art
import utilities as util
import pygame
import crew
import math


class Ship(object):
    """
    Attributes
    ----------
    speed
        Gotta go fast.
        Reverse engineer the move timer formula
        self.move_timer_max = round((5.0 / self.ship.speed) * 10)
        speed of 5.0 will result in 10 days to move from tile to tile,
        speed of 50 will result in 1 day per tile
        speed of 1.3 will result in 30 days per tile for movement
    cargo_cap : int
        Max Loaded Cargo in Tons.  Less loaded cargo increases speed, but this has
        not been implemented.
    crew_cap :int
        Maximum number of crew the ship can support.  Ships have a minimum needed, but
        additional crew can be taken on to increase speed, attack/defense power, etc.
        For now this does nothing, and crew is always at cap maximum.
    defense : int
        Defensive power of the ship.  Ability to resist cannon shots and repel
        boarders during attacks.  Negates incoming attack power
    attack : int
        Attack Power (cannons, small arms, etc).  Think Warhammer.
    wounds : int
        for combat purposes.
        Multiple wounds means you can fail more than one defense roll during
        combat before losing the ship.  Again, think Warhammer.
    purchase_cost : int
        Self Explanatory.
    """
    hull_class = None

    def __init__(self,
                 active_map,
                 column,
                 row,
                 speed,
                 cargo_cap,
                 crew_cap,
                 defense,
                 attack,
                 wounds,
                 purchase_cost):
        self.column = column  # int
        self.row = row  # int
        self.cargo_cap = cargo_cap  # int
        self.crew_cap = crew_cap  # int
        self.crew = {}  # dict[]
        self.speed = speed  # float
        self.defense = defense  # float
        self.attack = attack  # float
        self.purchase_cost = purchase_cost  # int
        self.wounds = wounds  # int
        self.upkeep = purchase_cost * 0.025  # float

        self.active_map = active_map  # GameMap
        """tile ID of current tile"""
        self.tile = None
        # laden_speed = base_speed * (0.5 * (1.0 - cargo_cap / current_cargo))
        self.cargo = {}  # dict[string] = int
        self.facing = 0

        self.set_image()

    def set_display_coordinates(self, tile_x: int, tile_y: int) -> None:
        self.x = tile_x
        self.y = tile_y

    def get_upkeep_cost(self):
        u = self.purchase_cost * 0.025
        return u + sum(quantity * crew.wages[sailor_name]
                       for sailor_name, quantity in self.crew.items())

    def get_vitals(self):
        vitals = {}
        for attr_name in ("column",
                          "row",
                          "cargo",
                          "hull_class"):
            vitals[attr_name] = getattr(self, attr_name)

        return vitals

    def load_external(self, records):
        for attr_name in ("column",
                          "row",
                          "cargo"):
            setattr(self, attr_name, records[attr_name])

    def set_facing(self, new_position):
        facings = {(-1, -1): 0,
                   (0, -1): 1,
                   (1, -1): 2,
                   (1, 0): 3,
                   (1, 1): 4,
                   (0, 1): 5,
                   (-1, 1): 6,
                   (-1, 0): 7,
                   (0, 0): self.facing}
        diff = (new_position[0] - self.column, new_position[1] - self.row)
        self.facing = facings[diff]

    def set_image(self):
        self.image = pygame.Surface([50, 50])
        self.image.fill(util.colors.key)
        self.image.blit(
            art.ships[self.hull_class],
            [0, 0],
            [self.facing * 50, 0, 50, 50])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()


# Bremen
class Cog(Ship):
    hull_class = "Cog"

    def __init__(self, active_map, column, row):
        super().__init__(
            active_map,
            column,
            row,
            speed=5,
            cargo_cap=50,
            crew_cap=15,
            defense=10,
            attack=10,
            wounds=1,
            purchase_cost=1000)


# Santa Maria
class Caravel(Ship):
    hull_class = "Caravel"

    def __init__(self, active_map, column, row):
        super().__init__(
            active_map, column, row,
            speed=5,
            cargo_cap=100,
            crew_cap=40,
            defense=15,
            attack=12,
            wounds=2,
            purchase_cost=5000)


class Argosy(Ship):
    hull_class = "Argosy"

    def __init__(self, active_map, column, row):
        super().__init__(
            active_map, column, row,
            speed=3.3,
            cargo_cap=200,
            crew_cap=40,
            defense=11,
            attack=12,
            wounds=2,
            purchase_cost=2500)


# On 6 April 1522, Trinidad left Tidore loaded with 50 tons of cloves.
#  Trinidad
# A typical three-masted carrack such as the São Gabriel had six sails: bowsprit, foresail, mainsail, mizzensail and two topsails. 

class Carrack(Ship):
    hull_class = "Carrack"

    def __init__(self, active_map, column, row):
        super().__init__(
            active_map, column, row,
            speed=5,
            cargo_cap=150,
            crew_cap=60,
            defense=11,
            attack=15,
            wounds=2,
            purchase_cost=6000)


class Nao(Ship):
    hull_class = "Nao"

    def __ini__(self, active_map, column, row):
        super().__init__(
            active_map, column, row,
            speed=5,
            cargo_cap=1000,
            crew_cap=200,
            defense=12,
            attack=15,
            wounds=3,
            purchase_cost=20000)


class Galleon(Ship):
    hull_class = "Galleon"

    def __init__(self, active_map, column, row):
        super().__init__(
            active_map, column, row,
            speed=6.25,
            cargo_cap=500,
            crew_cap=175,
            defense=25,
            attack=30,
            wounds=3,
            purchase_cost=12000)


# Hector
class Fluyt(Ship):
    hull_class = "Fluyt"

    def __init__(self, active_map, column, row):
        super().__init__(
            active_map, column, row,
            speed=8.34,
            cargo_cap=250,
            crew_cap=25,
            defense=12,
            attack=10,
            wounds=2,
            purchase_cost=12000)


class Corvette(Ship):
    hull_class = "Corvette"

    def __init__(self, active_map, column, row):
        super().__init__(
            active_map, column, row,
            speed=8.34,
            cargo_cap=100,
            crew_cap=100,
            defense=35,
            attack=30,
            wounds=3,
            purchase_cost=12000)


class Frigate(Ship):
    hull_class = "Frigate"

    def __init__(self, active_map, column, row):
        super().__init__(
            active_map, column, row,
            speed=6.25,
            cargo_cap=100,
            crew_cap=175,
            defense=30,
            attack=40,
            wounds=5,
            purchase_cost=20000)


class ShipOfTheLine(Ship):
    hull_class = "Ship of the Line"

    def __init__(self, active_map, column, row):
        super().__init__(
            active_map, column, row,
            speed=5,
            cargo_cap=500,
            crew_cap=600,
            defense=100,
            attack=125,
            wounds=10,
            purchase_cost=100000)


ship_types = {
    "Cog": Cog,
    "Carrack": Carrack,
    "Caravel": Caravel,
    "Argosy": Argosy,
    "Galleon": Galleon,
    "Fluyt": Fluyt,
    "Corvette": Corvette,
    "Frigate": Frigate,
    "Ship of the Line": ShipOfTheLine}
