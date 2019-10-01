import artikel

food_value = {"taiga": 1,
              "tundra": 1,
              "snowy tundra": 0,
              "grassland": 3,
              "plains": 2,
              "wet plains": 2,
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

terrain_food_value = {"river": 3,
                      "vegetation": 0,
                      "low hill": 0,
                      "hill": 0,
                      "low mountain": 0.0,
                      "mountain": 0.0}


wood_value = {"taiga": 1,
              "tundra": 0,
              "snowy tundra": 0,
              "grassland": 1,
              "plains": 0,
              "wet plains": 1,
              "savannah": 1,
              "desert": 0,
              "forest": 2,
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


biome_artikels = {}
terrain_artikels = {}

terrain_artikels["river"] = {"fish": 3}

terrain_artikels["low hill"] = {
    "iron": 4,
    "jewels": 1,
    "gold": 1,
    "silver": 1}

terrain_artikels["hill"] = {
    "iron": 3,
    "jewels": 2,
    "gold": 1,
    "silver": 1}

terrain_artikels["low mountain"] = {
    "iron": 3,
    "gold": 1,
    "silver": 3}

terrain_artikels["mountain"] = {
    "iron": 2,
    "gold": 3,
    "silver": 3}


for each_biome in food_value:
    biome_artikels[each_biome] = {}
    for each_artikel in artikel.all_resources:
        biome_artikels[each_biome][each_artikel] = 0

biome_artikels["taiga"] = {
    "wool": 1,
    "pelts": 1,
    "iron": 1,
    "silver": 1}
biome_artikels["tundra"] = {
    "pelts": 1,
    "silver": 1}
biome_artikels["snowy tundra"] = {
    "pelts": 1}
biome_artikels["grassland"] = {
    "cattle": 10,
    "wool": 10,
    "wheat": 10,
    "iron": 10,
    "silver": 1}
biome_artikels["plains"] = {
    "saffron": 1,
    "cinnamon": 1,
    "cattle": 1,
    "wheat": 1}
biome_artikels["wet plains"] = {
    "cinnamon": 1,
    "cattle": 1,
    "wheat": 1}
biome_artikels["savannah"] = {
    "ivory": 1,
    "cinnamon": 1,
    "gold": 1}
biome_artikels["desert"] = {
    "gold": 1,
    "jewels": 1}
biome_artikels["forest"] = {
    "timber": 1,
    "pelts": 1}
biome_artikels["jungle"] = {
    "clove": 1,
    "timber": 1}
biome_artikels["snowpack"] = {}
biome_artikels["ice"] = {}
biome_artikels["shrubland"] = {
    "wool": 1,
    "silver": 1,
    "iron": 1,
    "jewels": 1}
biome_artikels["ocean"] = {
    "ivory": 1,
    "fish": 1}
biome_artikels["sea"] = {
    "fish": 1,
    "shellfish": 1}
biome_artikels["shallows"] = {
    "fish": 1,
    "shellfish": 1}
biome_artikels["lake"] = {
    "fish": 1}




