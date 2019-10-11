import artikel

food_value = {"taiga": 1,
              "conifer": 1,
              "alpine": 1,
              "tundra": 1,
              "snowy tundra": 0,
              "grassland": 3,
              "plains": 3,
              "wet plains": 3,
              "savannah": 1,
              "desert": 0,
              "forest": 1,
              "jungle": 1,
              "snowpack": 0,
              "ice": 0,
              "shrubland": 1,
              "ocean": 2,
              "sea": 2,
              "shallows": 2,
              "lake": 1}

terrain_food_value = {"river": 1,
                      "vegetation": 0,
                      "low hill": 0,
                      "hill": 0,
                      "low mountain": 0.0,
                      "mountain": 0.0}


wood_value = {"taiga": 2,
              "conifer": 2,
              "alpine": 2,
              "tundra": 0,
              "snowy tundra": 0,
              "grassland": 0,
              "plains": 0,
              "wet plains": 1,
              "savannah": 1,
              "desert": 0,
              "forest": 3,
              "jungle": 2,
              "snowpack": 0,
              "ice": 0,
              "shrubland": 1,
              "ocean": 0,
              "sea": 0,
              "shallows": 0,
              "lake": 0}


terrain_wood_value = {"river": 0,
                      "vegetation": 0,
                      "low hill": 0,
                      "hill": 0,
                      "low mountain": 0.0,
                      "mountain": 0.0}


terrain_artikels = {}
biome_artikels = {}
resource_artikels = {}

terrain_artikels["river"] = {"fish": 1}

terrain_artikels["vegetation"] = {}

terrain_artikels["low hill"] = {
    "iron": 2}

terrain_artikels["hill"] = {
    "iron": 3}

terrain_artikels["low mountain"] = {
    "iron": 3}

terrain_artikels["mountain"] = {
    "iron": 2}


biome_artikels["taiga"] = {
    "wool": 1,
    "meat": 5,
    "pelts": 4,
    "iron": 1,
    "wood": 3}
biome_artikels["conifer"] = {
    "wool": 3,
    "meat": 3,
    "pelts": 2,
    "iron": 1,
    "wood": 4}
biome_artikels["tundra"] = {
    "pelts": 2,
    "meat": 1,
    "iron": 1}
biome_artikels["snowy tundra"] = {
    "meat": 1,
    "pelts": 3}
biome_artikels["alpine"] = {
    "pelts": 3,
    "meat": 1,
    "iron": 2}
biome_artikels["grassland"] = {
    "meat": 5,
    "wool": 10,
    "grain": 3}
biome_artikels["plains"] = {
    "meat": 2,
    "grain": 6}
biome_artikels["wet plains"] = {
    "meat": 3,
    "grain": 5}
biome_artikels["savannah"] = {
    "meat": 1,
    "grain": 5}
biome_artikels["desert"] = {
    "iron": 1}
biome_artikels["forest"] = {
    "wood": 10,
    "meat": 2,
    "iron": 1,
    "pelts": 2}
biome_artikels["jungle"] = {
    "fruit": 5,
    "meat": 1,
    "wood": 10}
biome_artikels["snowpack"] = {
    "meat": 1,
    "pelts": 1}
biome_artikels["ice"] = {}
biome_artikels["shrubland"] = {
    "wool": 2,
    "meat": 3}
biome_artikels["ocean"] = {
    "fish": 5,
    "shellfish": 1}
biome_artikels["sea"] = {
    "fish": 4,
    "shellfish": 2}
biome_artikels["shallows"] = {
    "fish": 3,
    "shellfish": 3}
biome_artikels["lake"] = {
    "fish": 5,
    "shellfish": 1}


all__resources = ["cattle",
                  "cinnamon",
                  "clove",
                  "fish",
                  "fruit",
                  "gold",
                  "wheat",
                  "iron",
                  "ivory",
                  "jewels",
                  "pelts",
                  "saffron",
                  "shellfish",
                  "silver",
                  "timber",
                  "wool"]

all_artikels = ["meat",
                "cinnamon",
                "clove",
                "fish",
                "fruit",
                "gold",
                "grain",
                "iron",
                "ivory",
                "jewels",
                "pelts",
                "saffron",
                "shellfish",
                "silver",
                "wood",
                "wool"]

resource_artikels["cattle"] = {"meat": 5}
resource_artikels["cinnamon"] = {"cinnamon": 10}
resource_artikels["clove"] = {"clove": 10}
resource_artikels["fish"] = {"fish": 5}
resource_artikels["fruit"] = {"fruit": 10}
resource_artikels["gold"] = {"gold": 5}
resource_artikels["wheat"] = {"grain": 10}
resource_artikels["iron"] = {"iron": 10}
resource_artikels["ivory"] = {"ivory": 5}
resource_artikels["jewels"] = {"jewels": 5}
resource_artikels["pelts"] = {"pelts": 5}
resource_artikels["saffron"] = {"saffron": 10}
resource_artikels["shellfish"] = {"shellfish": 10}
resource_artikels["silver"] = {"silver": 5}
resource_artikels["timber"] = {"wood": 10}
resource_artikels["wool"] = {"wool": 10}
resource_artikels[None] = {}


def set_output(chosen_tile):
    o = {}
    for artikel_id in all_artikels:
        o[artikel_id] = 0
    for artikel_dict in [biome_artikels[chosen_tile.biome],
                         terrain_artikels[chosen_tile.terrain],
                         resource_artikels[chosen_tile.resource]]:
        for artikel_id, value in artikel_dict.items():
            o[artikel_id] += value
    chosen_tile.output = o


def get_food_value(chosen_tile):
    f = 0
    for artikel_id in ["fish", "fruit", "grain", "meat", "shellfish"]:
        f += chosen_tile.output[artikel_id]
    return f









