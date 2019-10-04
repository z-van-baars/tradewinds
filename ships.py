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
            self.attr_name = records[attr_name]


class Cog(Ship):
    hull_class = "Cog"

    def __init__(self, active_map, column, row):
        super().__init__(
            active_map,
            column,
            row,
            speed=25,
            cargo_cap=50,
            crew_cap=10,
            defense=10,
            attack=10,
            wounds=1,
            purchase_cost=1000)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.cog_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()


class Carrack(Ship):
    hull_class = "Carrack"

    def __init__(self, active_map, column, row):
        super().__init__(active_map, column, row, 3, 150, 20, 11, 15, 2, 2000)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.carrack_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()


class Argosy(Ship):
    hull_class = "Argosy"

    def __init__(self, active_map, column, row):
        super().__init__(active_map, column, row, 3, 200, 25, 11, 12, 2, 2500)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.argosy_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()


class Caravel(Ship):
    hull_class = "Caravel"

    def __init__(self, active_map, column, row):
        super().__init__(active_map, column, row, 3, 300, 30, 15, 15, 2, 5000)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.caravel_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()


class Galleon(Ship):
    hull_class = "Galleon"

    def __init__(self, active_map, column, row):
        super().__init__(active_map, column, row, 3.2, 500, 50, 25, 25, 3, 10000)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.galleon_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()


class Fluyt(Ship):
    hull_class = "Fluyt"

    def __init__(self, active_map, column, row):
        super().__init__(active_map, column, row, 3, 750, 25, 12, 10, 2, 10000)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.fluyt_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()


class Corvette(Ship):
    hull_class = "Corvette"

    def __init__(self, active_map, column, row):
        super().__init__(active_map, column, row, 3, 250, 50, 25, 40, 3, 12000)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.corvette_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()


ship_types = {
    "Cog": Cog,
    "Carrack": Carrack,
    "Caravel": Caravel,
    "Argosy": Argosy,
    "Galleon": Galleon,
    "Fluyt": Fluyt,
    "Corvette": Corvette}
