from enum import Enum

#Resources = Enum('Resources', 'Saffron,Cinnamon,Vanilla,Clove,Ivory,Fine_Timber,Wool,Pelts,Cattle,Rice,Wheat,Iron,Gold,Silver')

Wood = ["forest", "jungle", "low hills", "hills", "alpine"]

Grain = ["grassland", "plains"]

Wool = ["shrubland", "grassland", "low hills"]

Cattle = ["grassland", "plains"]

Fruit = ["jungle"]

Saffron = ["plains", "savannah"]

Cinnamon = ["plains", "savannah", "low hills"]

Clove = ["jungle", "low hills"]

Ivory = ["savannah", "ocean"]

Shellfish = ["shallows", "sea", "ocean"]

Fish = ["shallows", "sea", "lake"]

Pelts = ["taiga", "tundra", "snowpack", "ice", "low hills", "alpine"]


Iron = [
    "grassland",
    "taiga",
    "alpine",
    "plains",
    "low hills",
    "hills",
    "low mountains",
    "mountains"]

Gold = [
    "plains",
    "shrubland",
    "savannah",
    "low hills",
    "hills",
    "low mountains",
    "mountains"]

Silver = [
    "grassland",
    "taiga",
    "alpine",
    "low hills",
    "hills",
    "low mountains",
    "mountains"]


Jewels = [
    "desert",
    "shrubland",
    "taiga",
    "low hills",
    "hills"]

rare_resources = ["saffron",
                  "cinnamon",
                  "clove",
                  "ivory",
                  "pelts",
                  "gold",
                  "silver",
                  "jewels"]


common_resources = ["timber",
                    "wool",
                    "iron"]

food_resources = ["cattle",
                  "wheat",
                  "fruit",
                  "fish",
                  "shellfish"]

all_resources = food_resources + common_resources + rare_resources

all_artikels = []


mountain = {"taiga": ["iron", "silver", "gold"],
            "tundra": ["iron", "silver"],
            "snowy tundra": ["iron", "silver"],
            "alpine": ["iron", "silver"],
            "grassland": ["iron", "silver", "gold"],
            "plains": ["iron", "silver", "gold"],
            "wet plains": ["iron", "silver", "gold"],
            "savannah": ["iron", "silver", "gold"],
            "desert": ["iron", "silver", "gold"],
            "forest": ["iron", "silver", "gold"],
            "conifer": ["iron", "silver", "gold"],
            "jungle": ["iron", "silver", "gold"],
            "snowpack": ["iron", "silver"],
            "ice": [None],
            "shrubland": ["iron", "silver", "gold"],
            "ocean": [None],
            "sea": [None],
            "shallows": [None],
            "lake": [None]}

low_mountain = {"taiga": ["iron", "silver", "gold"],
                "tundra": ["iron", "silver"],
                "snowy tundra": ["iron", "silver"],
                "alpine": ["iron", "silver"],
                "grassland": ["iron", "silver", "gold"],
                "plains": ["iron", "silver", "gold"],
                "wet plains": ["iron", "silver", "gold"],
                "savannah": ["iron", "silver", "gold"],
                "desert": ["iron", "silver", "gold"],
                "forest": ["iron", "silver", "gold"],
                "conifer": ["iron", "silver", "gold"],
                "jungle": ["iron", "silver", "gold"],
                "snowpack": ["iron", "silver"],
                "ice": [None],
                "shrubland": ["iron", "silver", "gold"],
                "ocean": [None],
                "sea": [None],
                "shallows": [None],
                "lake": [None]}

hill = {"taiga": ["iron", "silver", "jewels"],
        "tundra": ["iron", "silver"],
        "snowy tundra": ["iron", "silver"],
        "alpine": ["iron", "silver"],
        "grassland": ["iron", "silver", "gold"],
        "plains": ["iron", "silver", "gold"],
        "wet plains": ["iron", "silver", "gold"],
        "savannah": ["iron", "silver", "gold"],
        "desert": ["iron", "silver", "gold", "jewels"],
        "forest": ["iron", "silver", "gold"],
        "conifer": ["iron", "silver", "gold"],
        "jungle": ["iron", "silver", "gold"],
        "snowpack": ["iron", "silver"],
        "ice": [None],
        "shrubland": ["iron", "silver", "gold", "jewels"],
        "ocean": [None],
        "sea": [None],
        "shallows": [None],
        "lake": [None]}

low_hill = {"taiga": ["iron", "silver", "jewels"],
            "tundra": ["iron", "silver"],
            "snowy tundra": ["iron", "silver"],
            "alpine": ["iron", "silver"],
            "grassland": ["iron", "silver", "gold"],
            "plains": ["iron", "silver", "gold"],
            "wet plains": ["iron", "silver", "gold"],
            "savannah": ["iron", "silver", "gold"],
            "desert": ["iron", "silver", "gold", "jewels"],
            "forest": ["iron", "silver", "gold"],
            "conifer": ["iron", "silver", "gold"],
            "jungle": ["iron", "silver", "gold"],
            "snowpack": ["iron", "silver"],
            "ice": [None],
            "shrubland": ["iron", "silver", "gold", "jewels"],
            "ocean": [None],
            "sea": [None],
            "shallows": [None],
            "lake": [None]}


vegetation = {"taiga": ["wool", "pelts", "iron", "silver"],
              "tundra": ["pelts", "silver"],
              "snowy tundra": ["pelts"],
              "alpine": ["timber", "pelts", "iron"],
              "grassland": ["cattle", "wool", "wheat", "iron", "silver"],
              "plains": ["saffron", "cinnamon", "cattle", "wheat"],
              "wet plains": ["cinnamon", "cattle", "wheat"],
              "savannah": ["ivory", "cinnamon", "gold"],
              "desert": ["gold", "jewels"],
              "forest": ["timber", "pelts"],
              "conifer": ["timber", "pelts"],
              "jungle": ["clove", "timber", "fruit"],
              "snowpack": [None],
              "ice": [None],
              "shrubland": ["wool", "silver", "iron", "jewels"],
              "ocean": ["ivory", "fish"],
              "sea": ["fish", "shellfish"],
              "shallows": ["fish", "shellfish"],
              "lake": ["fish"]}

river = {"taiga": [None],
         "tundra": [None],
         "snowy tundra": [None],
         "alpine": [None],
         "grassland": [None],
         "plains": [None],
         "wet plains": [None],
         "savannah": [None],
         "desert": [None],
         "forest": [None],
         "conifer": [None],
         "jungle": [None],
         "snowpack": [None],
         "ice": [None],
         "shrubland": [None],
         "ocean": [None],
         "sea": [None],
         "shallows": [None],
         "lake": [None]}


possible_resources = {"river": river,
                      "vegetation": vegetation,
                      "low hill": low_hill,
                      "hill": hill,
                      "low mountain": low_mountain,
                      "mountain": mountain}


class Resource(object):
    biomes_allowed = {}
    terrain_allowed = {}


class Artikel(object):

    biome_production = {}
    terrain_production = {}
