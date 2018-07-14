

Saffron = ["plains", "savannah"]

Cinnamon = ["plains", "savannah", "low hills"]

Vanilla = ["jungle", "low hills"]

Clove = ["jungle", "low hills"]

Ivory = ["savannah"]

Fine_Timber = ["forest", "jungle", "low hills", "hills"]

Wool = ["shrubland", "grassland", "low hills"]

Pelts = ["taiga", "tundra", "low hills"]

Cattle = ["grassland", "plains"]

Rice = ["grassland", "jungle", "low hills", "hills"]

Wheat = ["grassland", "plains"]

Iron = ["grassland", "taiga", "plains", "low hills", "hills", "low mountains", "mountains"]

Gold = ["plains", "shrubland", "savannah", "low hills", "hills", "low mountains", "mountains"]

Silver = ["grassland", "taiga", "low hills", "hills", "low mountains", "mountains"]


all_resources = ["saffron",
                 "cinnamon",
                 "vanilla",
                 "clove",
                 "ivory",
                 "timber",
                 "wool",
                 "pelts",
                 "cattle",
                 "rice",
                 "wheat",
                 "iron",
                 "gold",
                 "silver"]


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
            "lake": [None],
            "river": [None]}

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
                "lake": [None],
                "river": [None]}

hill = {"taiga": ["iron", "silver"],
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
        "lake": [None],
        "river": [None]}

low_hill = {"taiga": ["iron", "silver"],
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
            "lake": [None],
            "river": [None]}


vegetation = {"taiga": ["pelts", "iron", "silver"],
              "tundra": ["pelts"],
              "snowy tundra": ["pelts"],
              "grassland": ["cattle", "wool", "rice", "wheat", "iron", "silver"],
              "plains": ["saffron", "cinnamon", "cattle", "wheat"],
              "wet plains": ["cinnamon", "cattle", "wheat"],
              "savannah": ["ivory", "cinnamon", "gold"],
              "desert": ["gold"],
              "forest": ["timber", "pelts"],
              "jungle": ["clove", "vanilla", "timber", "rice"],
              "snowpack": [None],
              "ice": [None],
              "shrubland": ["wool", "silver", "iron"],
              "ocean": [None],
              "sea": [None],
              "shallows": [None],
              "lake": [None],
              "river": [None]}


possible_resources = {"vegetation": vegetation,
                      "low hill": low_hill,
                      "hill": hill,
                      "low mountain": low_mountain,
                      "mountain": mountain}

