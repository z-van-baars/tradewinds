import navigate


class Ship(object):
    def __init__(self, speed, cargo_cap, crew_cap, defense, attack, wounds, cost):
        self.cargo_cap = cargo_cap
        self.crew_cap = crew_cap
        self.defense = defense
        self.attack = attack
        self.cost = cost
        self.wounds = wounds

        self.x = 0
        self.y = 0
        self.node = None
        self.path = None
        self.target_node = None
        self.target_port = None
        self.speed = speed
        self.move_timer = 0
        self.cargo = {}

    def clear_target(self):
        self.target_node = None
        self.target_port = None
        self.path = None

    def set_display_coordinates(self, node_x, node_y):
        self.x = node_x
        self.y = node_y

    def check_move_timer(self):
        if self.move_timer <= 0:
            return True
        return False

    def move(self, nav_mesh):
        if self.target_node:
            if not self.path:
                self.path = navigate.get_path(self.node, nav_mesh, self.target_node)
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
