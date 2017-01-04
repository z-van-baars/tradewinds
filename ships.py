

class Ship(object):
    def __init__(self, speed, cargo_cap, crew_cap, defense, attack, wounds, cost):
        self.x = 0
        self.y = 0
        self.node = None
        self.speed = speed
        self.cargo_cap = cargo_cap
        self.crew_cap = crew_cap
        self.defense = defense
        self.attack = attack
        self.cost = cost
        self.wounds = wounds
        self.cargo = {}


class Cog(Ship):
    def __init__(self):
        super().__init__(10, 50, 10, 10, 10, 1, 1000)


class Carrack(Ship):
    def __init__(self):
        super().__init__(12, 150, 20, 11, 15, 2, 2000)


class Argosy(Ship):
    def __init__(self):
        super().__init__(12, 200, 25, 11, 12, 2, 2500)


class Caravel(Ship):
    def __init__(self):
        super().__init__(15, 300, 30, 15, 15, 2, 5000)


class Galleon(Ship):
    def __init__(self):
        super().__init__(12, 500, 50, 25, 25, 3, 10000)


class Fluyt(Ship):
    def __init__(self):
        super().__init__(15, 750, 25, 12, 10, 2, 10000)


class Corvette(Ship):
    def __init__(self):
        super().__init__(15, 250, 50, 25, 40, 3, 12000)
