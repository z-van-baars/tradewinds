import navigate
import art
import utilities as util
import pygame


class Ship(object):
    """
    Attributes
    ----------
    speed
        Gotta go fast.  For now this does nothing.
    cargo_cap : int
        Max Loaded Cargo in Tons.  Less loaded cargo increases speed, but this has
        not been implemented.
    crew_cap :int
        Maximum number of crew the ship can support.  Ships have a minimum needed, but
        additional crew can be taken on to increase speed, attack/defense power, etc.
        For now this does nothing, and crew is always at cap maximum.
    defense : int
        Defensive power of the ship.  Ability to resist cannon shots and repel boarders during
        attacks.  Negates incoming attack power
    attack : int
        Attack Power (cannons, small arms, etc).  Think Warhammer.
    wounds : int
        for combat purposes.  Multiple wounds means you can fail more than one defense roll during
        combat before losing the ship.  Again, think Warhammer.
    purchase_cost : int
        Self Explanatory.
    """

    def __init__(self, speed, cargo_cap, crew_cap, defense, attack, wounds, purchase_cost):
        self.cargo_cap = cargo_cap
        self.crew_cap = crew_cap
        self.speed = speed
        self.defense = defense
        self.attack = attack
        self.purchase_cost = purchase_cost
        self.wounds = wounds

        """x y pair for screen rendering"""
        self.x = 0
        self.y = 0
        """tile ID of current tile"""
        self.tile = None
        """path object.  Should be None if there is no target"""
        self.path = None
        """Target Tile ID (for now this will always be chained to the target port / port ID)"""
        self.target_tile = None
        self.target_port = None
        self.move_timer = 0
        """
        CARGO Dictionary
        Keys are plaintext names of commodities or spices, e.g. 'Nutmeg' and the value is a quantity in Int form"""
        self.cargo = {}

    def clear_target(self):
        self.target_tile = None
        self.target_port = None
        self.path = None

    def set_display_coordinates(self, tile_x: int, tile_y: int) -> None:
        self.x = tile_x
        self.y = tile_y

    def check_move_timer(self):
        if self.move_timer <= 0:
            return True
        return False

    def move(self, nav_mesh):
        if self.target_tile:
            if not self.path:
                self.path = navigate.get_path(self.tile, nav_mesh, self.target_tile)
                self.move_timer = self.path.edges[0].cost
            assert self.path
            assert self.path.steps
            ready_to_move = self.check_move_timer()
            if ready_to_move:
                assert len(self.path.edges) == len(self.path.steps)
                self.node = (self.path.steps.pop(0)).id_tag
                self.path.edges.pop(0)
                if self.path.edges:
                    self.move_timer = self.path.edges[0].cost
            else:
                self.move_timer -= 1

    def get_path(self):
        navigate.get_path()


class Cog(Ship):
    def __init__(self):
        super().__init__(
            speed=10,
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
        self.hull_class = "Cog"


class Carrack(Ship):
    def __init__(self):
        super().__init__(12, 150, 20, 11, 15, 2, 2000)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.carrack_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()
        self.hull_class = "Carrack"


class Argosy(Ship):
    def __init__(self):
        super().__init__(12, 200, 25, 11, 12, 2, 2500)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.argosy_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()
        self.hull_class = "Argosy"


class Caravel(Ship):
    def __init__(self):
        super().__init__(15, 300, 30, 15, 15, 2, 5000)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.caravel_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()
        self.hull_class = "Caravel"


class Galleon(Ship):
    def __init__(self):
        super().__init__(12, 500, 50, 25, 25, 3, 10000)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.galleon_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()
        self.hull_class = "Galleon"


class Fluyt(Ship):
    def __init__(self):
        super().__init__(15, 750, 25, 12, 10, 2, 10000)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.fluyt_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()
        self.hull_class = "Fluyt"


class Corvette(Ship):
    def __init__(self):
        super().__init__(15, 250, 50, 25, 40, 3, 12000)
        self.image = pygame.Surface([40, 40])
        self.image.fill(util.colors.key)
        self.image.blit(art.corvette_icon, [0, 0])
        self.image.set_colorkey(util.colors.key)
        self.image = self.image.convert_alpha()
        self.hull_class = "Corvette"
