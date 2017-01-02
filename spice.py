spices = {"Cinnamon": 1,
          "Pepper": 1,
          "Ginger": 1,
          "Turmeric": 1,
          "Cardomom": 1,
          "Saffron": 1,
          "Cloves": 1,
          "Nutmeg": 1,
          "Garlic": 1,
          "Anise": 1}


class Spice(object):
    def __init__(self, base_cost):
        self.base_cost = base_cost


class Saffron(Spice):
    def __init__(self):
        super().__init__(100)


class Ginger(Spice):
    def __init__(self):
        super().__init__(10)


class Cloves(Spice):
    def __init__(self):
        super().__init__(10)


class Cinnamon(Spice):
    def __init__(self):
        super().__init__(10)


class Nutmeg(Spice):
    def __init__(self):
        super().__init__(10)


class Garlic(Spice):
    def __init__(self):
        super().__init__(10)


class Cardomom(Spice):
    def __init__(self):
        super().__init__(20)


class Pepper(Spice):
    def __init__(self):
        super().__init__(5)


class Anise(Spice):
    def __init__(self):
        super().__init__(20)


class Turmeric(Spice):
    def __init__(self):
        super().__init__(15)

