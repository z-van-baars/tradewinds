import pygame
import utilities


pygame.init()
pygame.display.set_mode([0, 0])

key_color = utilities.colors.key


# ICONS
galleon_icon = pygame.image.load("art/icons/galleon_icon.png").convert_alpha()
cog_icon = pygame.image.load("art/icons/cog_icon.png").convert_alpha()
cog_icon.set_colorkey(key_color)
cog_icon = cog_icon.convert_alpha()
carrack_icon = pygame.image.load("art/icons/carrack_icon.png").convert_alpha()
carrack_icon.set_colorkey(key_color)
carrack_icon = carrack_icon.convert_alpha()
argosy_icon = pygame.image.load("art/icons/carrack_icon.png").convert_alpha()
argosy_icon.set_colorkey(key_color)
argosy_icon = argosy_icon.convert_alpha()
caravel_icon = pygame.image.load("art/icons/caravel_icon.png").convert_alpha()
caravel_icon.set_colorkey(key_color)
caravel_icon = caravel_icon.convert_alpha()
galleon_icon = pygame.image.load("art/icons/galleon_icon.png").convert_alpha()
galleon_icon.set_colorkey(key_color)
galleon_icon = galleon_icon.convert_alpha()


# BUTTONS
x_regular = pygame.image.load("art/buttons/x_regular.png").convert_alpha()
x_hover = pygame.image.load("art/buttons/x_hover.png").convert_alpha()

market_regular = pygame.image.load("art/buttons/market_regular.png").convert_alpha()
market_hover = pygame.image.load("art/buttons/market_hover.png").convert_alpha()

arrow_down_regular = pygame.image.load("art/buttons/arrow_down_regular.png").convert_alpha()
arrow_down_hover = pygame.image.load("art/buttons/arrow_down_hover.png").convert_alpha()

arrow_up_regular = pygame.image.load("art/buttons/arrow_up_regular.png").convert_alpha()
arrow_up_hover = pygame.image.load("art/buttons/arrow_up_hover.png").convert_alpha()

arrow_left_regular = pygame.image.load("art/buttons/arrow_left_regular.png").convert_alpha()
arrow_left_hover = pygame.image.load("art/buttons/arrow_left_hover.png").convert_alpha()

arrow_right_regular = pygame.image.load("art/buttons/arrow_right_regular.png").convert_alpha()
arrow_right_hover = pygame.image.load("art/buttons/arrow_right_hover.png").convert_alpha()

buy_regular = pygame.image.load("art/buttons/buy_regular.png").convert_alpha()
buy_hover = pygame.image.load("art/buttons/buy_hover.png").convert_alpha()

sell_regular = pygame.image.load("art/buttons/sell_regular.png").convert_alpha()
sell_hover = pygame.image.load("art/buttons/sell_hover.png").convert_alpha()

done_regular = pygame.image.load("art/buttons/done_regular.png").convert_alpha()
done_hover = pygame.image.load("art/buttons/done_hover.png").convert_alpha()

cancel_regular = pygame.image.load("art/buttons/cancel_regular.png").convert_alpha()
cancel_hover = pygame.image.load("art/buttons/cancel_hover.png").convert_alpha()

view_port_regular = pygame.image.load("art/buttons/view_port_regular.png").convert_alpha()
view_port_hover = pygame.image.load("art/buttons/view_port_hover.png").convert_alpha()

goto_regular = pygame.image.load("art/buttons/goto_regular.png").convert_alpha()
goto_hover = pygame.image.load("art/buttons/goto_hover.png").convert_alpha()

repair_regular = pygame.image.load("art/buttons/repair_regular.png").convert_alpha()
repair_hover = pygame.image.load("art/buttons/repair_hover.png").convert_alpha()


# MENUS
port_screen = pygame.image.load("art/menus/port_screen.png").convert_alpha()
market_screen = pygame.image.load("art/menus/market_screen.png").convert_alpha()
ship_status_screen = pygame.image.load("art/menus/ship_status.png").convert_alpha()
quantity_popup = pygame.image.load("art/menus/quantity_popup.png").convert_alpha()

mini_map_preview = pygame.image.load("art/menus/mini_map_bg.png").convert_alpha()

# RESOURCES
saffron = pygame.image.load("art/resources/saffron_1.png").convert_alpha()
saffron.set_colorkey(utilities.colors.key)
saffron = saffron.convert_alpha()
cinnamon = pygame.image.load("art/resources/cinnamon_1.png").convert_alpha()
cinnamon.set_colorkey(utilities.colors.key)
cinnamon = cinnamon.convert_alpha()
clove = pygame.image.load("art/resources/clove_1.png").convert_alpha()
clove.set_colorkey(utilities.colors.key)
clove = clove.convert_alpha()
vanilla = pygame.image.load("art/resources/vanilla_1.png").convert_alpha()
vanilla.set_colorkey(utilities.colors.key)
vanilla = vanilla.convert_alpha()
ivory = pygame.image.load("art/resources/ivory_1.png").convert_alpha()
ivory.set_colorkey(utilities.colors.key)
ivory = ivory.convert_alpha()
timber = pygame.image.load("art/resources/timber_1.png").convert_alpha()
timber.set_colorkey(utilities.colors.key)
timber = timber.convert_alpha()
wool = pygame.image.load("art/resources/wool_1.png").convert_alpha()
wool.set_colorkey(utilities.colors.key)
wool = wool.convert_alpha()
pelts = pygame.image.load("art/resources/pelts_1.png").convert_alpha()
pelts.set_colorkey(utilities.colors.key)
pelts = pelts.convert_alpha()
cattle = pygame.image.load("art/resources/cattle_1.png").convert_alpha()
cattle.set_colorkey(utilities.colors.key)
cattle = cattle.convert_alpha()
rice = pygame.image.load("art/resources/rice_1.png").convert_alpha()
rice.set_colorkey(utilities.colors.key)
rice = rice.convert_alpha()
wheat = pygame.image.load("art/resources/wheat_1.png").convert_alpha()
wheat.set_colorkey(utilities.colors.key)
wheat = wheat.convert_alpha()
iron = pygame.image.load("art/resources/iron_1.png").convert_alpha()
iron.set_colorkey(utilities.colors.key)
iron = iron.convert_alpha()
gold = pygame.image.load("art/resources/gold_1.png").convert_alpha()
gold.set_colorkey(utilities.colors.key)
gold = gold.convert_alpha()
silver = pygame.image.load("art/resources/silver_1.png").convert_alpha()
silver.set_colorkey(utilities.colors.key)
silver = silver.convert_alpha()

resource_images = {"saffron": [saffron],
                   "cinnamon": [cinnamon],
                   "clove": [clove],
                   "vanilla": [vanilla],
                   "ivory": [ivory],
                   "timber": [timber],
                   "wool": [wool],
                   "pelts": [pelts],
                   "cattle": [cattle],
                   "rice": [rice],
                   "wheat": [wheat],
                   "iron": [iron],
                   "gold": [gold],
                   "silver": [silver]}


# CONSTRUCTS

city_1 = pygame.image.load("art/constructs/city/ancient_city_1.png").convert_alpha()
city_1.set_colorkey(utilities.colors.key)
city_1 = city_1.convert_alpha()
city_2 = pygame.image.load("art/constructs/city/ancient_city_2.png").convert_alpha()
city_2.set_colorkey(utilities.colors.key)
city_2 = city_2.convert_alpha()
city_3 = pygame.image.load("art/constructs/city/ancient_city_3.png").convert_alpha()
city_3.set_colorkey(utilities.colors.key)
city_3 = city_3.convert_alpha()


# TILES
grass_tile = pygame.image.load("art/tiles/grassland_1.png").convert_alpha()
grass_tile.set_colorkey(utilities.colors.key)
grass_tile = grass_tile.convert_alpha()

ice_tile = pygame.image.load("art/tiles/ice_1.png").convert_alpha()
ice_tile.set_colorkey(utilities.colors.key)
ice_tile = ice_tile.convert_alpha()

ocean_tile = pygame.image.load("art/tiles/ocean_1.png").convert_alpha()
ocean_tile.set_colorkey(utilities.colors.key)
ocean_tile = ocean_tile.convert_alpha()

river_tile = pygame.image.load("art/tiles/ocean_1.png").convert_alpha()
river_tile.set_colorkey(utilities.colors.key)
river_tile = river_tile.convert_alpha()

lake_tile = pygame.image.load("art/tiles/ocean_1.png").convert_alpha()
lake_tile.set_colorkey(utilities.colors.key)
lake_tile = lake_tile.convert_alpha()

tundra_tile = pygame.image.load("art/tiles/tundra_1.png").convert_alpha()
tundra_tile.set_colorkey(utilities.colors.key)
tundra_tile = tundra_tile.convert_alpha()

snowy_tundra_tiles_raw = [pygame.image.load("art/tiles/snowy_tundra_1.png").convert_alpha(),
                          pygame.image.load("art/tiles/snowy_tundra_2.png").convert_alpha(),
                          pygame.image.load("art/tiles/snowy_tundra_3.png").convert_alpha()]
snowy_tundra_tiles = []
for each in snowy_tundra_tiles_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snowy_tundra_tiles.append(each)

shrubland_tile = pygame.image.load("art/tiles/shrubland_1.png").convert_alpha()
shrubland_tile.set_colorkey(utilities.colors.key)
shrubland_tile = shrubland_tile.convert_alpha()

taiga_tile = pygame.image.load("art/tiles/taiga_1.png").convert_alpha()
taiga_tile.set_colorkey(utilities.colors.key)
taiga_tile = taiga_tile.convert_alpha()

jungle_tile = pygame.image.load("art/tiles/jungle_1.png").convert_alpha()
jungle_tile.set_colorkey(utilities.colors.key)
jungle_tile = jungle_tile.convert_alpha()

forest_tile = pygame.image.load("art/tiles/forest_1.png").convert_alpha()
forest_tile.set_colorkey(utilities.colors.key)
forest_tile = forest_tile.convert_alpha()

grassland_tile = pygame.image.load("art/tiles/grassland_1.png").convert_alpha()
grassland_tile.set_colorkey(utilities.colors.key)
grassland_tile = grassland_tile.convert_alpha()

desert_tile = pygame.image.load("art/tiles/desert_1.png").convert_alpha()
desert_tile.set_colorkey(utilities.colors.key)
desert_tile = desert_tile.convert_alpha()

plains_tile = pygame.image.load("art/tiles/plains_1.png").convert_alpha()
plains_tile.set_colorkey(utilities.colors.key)
plains_tile = plains_tile.convert_alpha()


snowpack_images_raw = [pygame.image.load("art/tiles/snowpack_1.png").convert_alpha(),
                       pygame.image.load("art/tiles/snowpack_2.png").convert_alpha(),
                       pygame.image.load("art/tiles/snowpack_3.png").convert_alpha(),
                       pygame.image.load("art/tiles/snowpack_4.png").convert_alpha()]
snowpack_images = []

for each in snowpack_images_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snowpack_images.append(each)

savannah_images_raw = [pygame.image.load("art/tiles/savannah_1.png").convert_alpha(),
                       pygame.image.load("art/tiles/savannah_2.png").convert_alpha(),
                       pygame.image.load("art/tiles/savannah_3.png").convert_alpha()]

savannah_images = []
for each in savannah_images_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    savannah_images.append(each)

desert_images_raw = [pygame.image.load("art/tiles/desert_1.png").convert_alpha(),
                     pygame.image.load("art/tiles/desert_2.png").convert_alpha(),
                     pygame.image.load("art/tiles/desert_3.png").convert_alpha(),
                     pygame.image.load("art/tiles/desert_4.png").convert_alpha()]


desert_images = []
for each in desert_images_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    desert_images.append(each)


# TERRAIN
tree_1 = pygame.image.load("art/constructs/terrain/tree_1.png").convert_alpha()
forest_1 = pygame.image.load("art/terrain/forest_1.png").convert_alpha()
forest_1.set_colorkey(utilities.colors.key)
forest_1 = forest_1.convert_alpha()

grassland_mountains_raw = [pygame.image.load("art/terrain/mountains/grassland_1.png").convert_alpha(),
                           pygame.image.load("art/terrain/mountains/grassland_2.png").convert_alpha(),
                           pygame.image.load("art/terrain/mountains/grassland_3.png").convert_alpha(),
                           pygame.image.load("art/terrain/mountains/grassland_4.png").convert_alpha(),
                           pygame.image.load("art/terrain/mountains/grassland_5.png").convert_alpha(),
                           pygame.image.load("art/terrain/mountains/grassland_6.png").convert_alpha()]


grassland_mountains = []
for each in grassland_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    grassland_mountains.append(each)

snow_mountains_raw = [pygame.image.load("art/terrain/mountains/snowy_tundra_1.png").convert_alpha(),
                      pygame.image.load("art/terrain/mountains/snowy_tundra_2.png").convert_alpha(),
                      pygame.image.load("art/terrain/mountains/snowy_tundra_3.png").convert_alpha(),
                      pygame.image.load("art/terrain/mountains/snowy_tundra_4.png").convert_alpha(),
                      pygame.image.load("art/terrain/mountains/snowy_tundra_5.png").convert_alpha(),
                      pygame.image.load("art/terrain/mountains/snowy_tundra_6.png").convert_alpha()]


snow_mountains = []
for each in snow_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snow_mountains.append(each)


grassland_low_mountains_raw = [pygame.image.load("art/terrain/low_mountains/grassland_1.png").convert_alpha(),
                               pygame.image.load("art/terrain/low_mountains/grassland_2.png").convert_alpha(),
                               pygame.image.load("art/terrain/low_mountains/grassland_3.png").convert_alpha()]


grassland_low_mountains = []
for each in grassland_low_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    grassland_low_mountains.append(each)


snow_low_mountains_raw = [pygame.image.load("art/terrain/low_mountains/snowy_tundra_1.png").convert_alpha(),
                          pygame.image.load("art/terrain/low_mountains/snowy_tundra_2.png").convert_alpha(),
                          pygame.image.load("art/terrain/low_mountains/snowy_tundra_3.png").convert_alpha()]


snow_low_mountains = []
for each in snow_low_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snow_low_mountains.append(each)


grassland_hills_raw = [pygame.image.load("art/terrain/hills/grassland_1.png").convert_alpha(),
                       pygame.image.load("art/terrain/hills/grassland_2.png").convert_alpha(),
                       pygame.image.load("art/terrain/hills/grassland_3.png").convert_alpha()]


grassland_hills = []
for each in grassland_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    grassland_hills.append(each)


snow_hills_raw = [pygame.image.load("art/terrain/hills/snowy_tundra_1.png").convert_alpha(),
                  pygame.image.load("art/terrain/hills/snowy_tundra_2.png").convert_alpha(),
                  pygame.image.load("art/terrain/hills/snowy_tundra_3.png").convert_alpha()]


snow_hills = []
for each in snow_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snow_hills.append(each)

grassland_low_hills_raw = [pygame.image.load("art/terrain/low_hills/grassland_1.png").convert_alpha(),
                           pygame.image.load("art/terrain/low_hills/grassland_2.png").convert_alpha(),
                           pygame.image.load("art/terrain/low_hills/grassland_3.png").convert_alpha(),
                           pygame.image.load("art/terrain/low_hills/grassland_4.png").convert_alpha()]


grassland_low_hills = []
for each in grassland_low_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    grassland_low_hills.append(each)

snow_low_hills_raw = [pygame.image.load("art/terrain/low_hills/snowy_tundra_1.png").convert_alpha(),
                      pygame.image.load("art/terrain/low_hills/snowy_tundra_2.png").convert_alpha(),
                      pygame.image.load("art/terrain/low_hills/snowy_tundra_3.png").convert_alpha(),
                      pygame.image.load("art/terrain/low_hills/snowy_tundra_4.png").convert_alpha()]

snow_low_hills = []
for each in snow_low_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snow_low_hills.append(each)

taiga_trees_raw = [pygame.image.load("art/terrain/taiga_1.png").convert_alpha(),
                   pygame.image.load("art/terrain/taiga_2.png").convert_alpha(),
                   pygame.image.load("art/terrain/taiga_3.png").convert_alpha()]


taiga_trees = []
for each in taiga_trees_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    taiga_trees.append(each)


wet_plains_trees_raw = [pygame.image.load("art/terrain/wet_plains_trees_1.png").convert_alpha(),
                        pygame.image.load("art/terrain/wet_plains_trees_2.png").convert_alpha(),
                        pygame.image.load("art/terrain/wet_plains_trees_3.png").convert_alpha()]


wet_plains_trees = []
for each in wet_plains_trees_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    wet_plains_trees.append(each)

jungle_trees_raw = [pygame.image.load("art/terrain/jungle_trees_1.png").convert_alpha(),
                    pygame.image.load("art/terrain/jungle_trees_2.png").convert_alpha(),
                    pygame.image.load("art/terrain/jungle_trees_3.png").convert_alpha(),
                    pygame.image.load("art/terrain/jungle_trees_4.png").convert_alpha(),
                    pygame.image.load("art/terrain/jungle_trees_5.png").convert_alpha(),
                    pygame.image.load("art/terrain/jungle_trees_6.png").convert_alpha(),
                    pygame.image.load("art/terrain/jungle_trees_7.png").convert_alpha()]


jungle_trees = []
for each in jungle_trees_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    jungle_trees.append(each)


# BUILDINGS
city_1 = pygame.image.load("art/constructs/city/ancient_city_1.png").convert_alpha()

biome_images = {"grass": [grass_tile],
                "grassland": [grassland_tile],
                "plains": [plains_tile],
                "wet plains": [plains_tile],
                "desert": desert_images,
                "forest": [forest_tile],
                "jungle": [jungle_tile],
                "tundra": [tundra_tile],
                "snowy tundra": snowy_tundra_tiles,
                "taiga": [taiga_tile],
                "snowpack": snowpack_images,
                "ice": [ice_tile],
                "savannah": savannah_images,
                "shrubland": [shrubland_tile],
                "ocean": [ocean_tile],
                "lake": [lake_tile],
                "river": [river_tile]}

mountains = {"taiga": snow_mountains,
             "tundra": snow_mountains,
             "snowy tundra": snow_mountains,
             "grassland": grassland_mountains,
             "plains": grassland_mountains,
             "wet plains": grassland_mountains,
             "savannah": grassland_mountains,
             "desert": grassland_mountains,
             "forest": grassland_mountains,
             "jungle": grassland_mountains,
             "snowpack": snow_mountains,
             "ice": snow_mountains,
             "shrubland": grassland_mountains,
             "ocean": grassland_mountains,
             "lake": grassland_mountains,
             "river": grassland_mountains}

low_mountains = {"taiga": snow_low_mountains,
                 "tundra": snow_low_mountains,
                 "snowy tundra": snow_low_mountains,
                 "grassland": grassland_low_mountains,
                 "plains": grassland_low_mountains,
                 "wet plains": grassland_low_mountains,
                 "savannah": grassland_low_mountains,
                 "desert": grassland_low_mountains,
                 "forest": grassland_low_mountains,
                 "jungle": grassland_low_mountains,
                 "snowpack": snow_low_mountains,
                 "ice": snow_low_mountains,
                 "shrubland": grassland_low_mountains,
                 "ocean": grassland_low_mountains,
                 "lake": grassland_low_mountains,
                 "river": grassland_low_mountains}

hills = {"taiga": grassland_hills,
         "tundra": snow_hills,
         "snowy tundra": snow_hills,
         "grassland": grassland_hills,
         "plains": grassland_hills,
         "wet plains": grassland_hills,
         "savannah": grassland_hills,
         "desert": grassland_hills,
         "forest": grassland_hills,
         "jungle": grassland_hills,
         "snowpack": snow_hills,
         "ice": snow_hills,
         "shrubland": grassland_hills,
         "ocean": grassland_hills,
         "lake": grassland_hills,
         "river": grassland_hills}

low_hills = {"taiga": grassland_low_hills,
             "tundra": snow_low_hills,
             "snowy tundra": snow_low_hills,
             "grassland": grassland_low_hills,
             "plains": grassland_low_hills,
             "wet plains": grassland_low_hills,
             "savannah": grassland_low_hills,
             "desert": grassland_low_hills,
             "forest": grassland_low_hills,
             "jungle": grassland_low_hills,
             "snowpack": snow_low_hills,
             "ice": snow_low_hills,
             "shrubland": grassland_low_hills,
             "ocean": grassland_low_hills,
             "lake": grassland_low_hills,
             "river": grassland_low_hills}


vegetation = {"taiga": taiga_trees,
              "tundra": None,
              "snowy tundra": None,
              "grassland": None,
              "plains": None,
              "wet plains": wet_plains_trees,
              "savannah": None,
              "desert": None,
              "forest": [forest_1],
              "jungle": jungle_trees,
              "snowpack": None,
              "ice": None,
              "shrubland": None,
              "ocean": None,
              "lake": None,
              "river": None}

terrain_images = {"mountain": mountains,
                  "low mountain": low_mountains,
                  "hill": hills,
                  "low hill": low_hills,
                  "vegetation": vegetation}
