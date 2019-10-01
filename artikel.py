from enum import Enum

#Resources = Enum('Resources', 'Saffron,Cinnamon,Vanilla,Clove,Ivory,Fine_Timber,Wool,Pelts,Cattle,Rice,Wheat,Iron,Gold,Silver')

Wood = ["forest", "jungle", "low hills", "hills"]

Grain = ["grassland", "plains"]

Wool = ["shrubland", "grassland", "low hills"]

Cattle = ["grassland", "plains"]

Saffron = ["plains", "savannah"]

Cinnamon = ["plains", "savannah", "low hills"]

Clove = ["jungle", "low hills"]

Ivory = ["savannah", "ocean"]

Shellfish = ["shallows", "sea", "ocean"]

Fish = ["shallows", "sea", "lake"]

Pelts = ["taiga", "tundra", "snowpack", "ice", "low hills"]


Iron = [
    "grassland",
    "taiga",
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


common_resources = ["wood",
                    "wool",
                    "iron"]

food_resources = ["cattle",
                  "grain",
                  "fish"]

all_resources = food_resources + common_resources + rare_resources


mountain = {"taiga": ["iron", "silver", "gold"],
            "tundra": ["iron", "silver"],
            "snowy tundra": ["iron", "silver"],
            "grassland": ["iron", "silver", "gold"],
            "plains": ["iron", "silver", "gold"],
            "wet plains": ["iron", "silver", "gold"],
            "savannah": ["iron", "silver", "gold"],
            "desert": ["iron", "silver", "gold"],
            "forest": ["iron", "silver", "gold"],
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
                "grassland": ["iron", "silver", "gold"],
                "plains": ["iron", "silver", "gold"],
                "wet plains": ["iron", "silver", "gold"],
                "savannah": ["iron", "silver", "gold"],
                "desert": ["iron", "silver", "gold"],
                "forest": ["iron", "silver", "gold"],
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
        "grassland": ["iron", "silver", "gold"],
        "plains": ["iron", "silver", "gold"],
        "wet plains": ["iron", "silver", "gold"],
        "savannah": ["iron", "silver", "gold"],
        "desert": ["iron", "silver", "gold", "jewels"],
        "forest": ["iron", "silver", "gold"],
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
            "grassland": ["iron", "silver", "gold"],
            "plains": ["iron", "silver", "gold"],
            "wet plains": ["iron", "silver", "gold"],
            "savannah": ["iron", "silver", "gold"],
            "desert": ["iron", "silver", "gold", "jewels"],
            "forest": ["iron", "silver", "gold"],
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
              "grassland": ["cattle", "wool", "wheat", "iron", "silver"],
              "plains": ["saffron", "cinnamon", "cattle", "wheat"],
              "wet plains": ["cinnamon", "cattle", "wheat"],
              "savannah": ["ivory", "cinnamon", "gold"],
              "desert": ["gold", "jewels"],
              "forest": ["timber", "pelts"],
              "jungle": ["clove", "timber"],
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
         "grassland": [None],
         "plains": [None],
         "wet plains": [None],
         "savannah": [None],
         "desert": [None],
         "forest": [None],
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
