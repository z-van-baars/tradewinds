import pygame
import utilities


pygame.init()
pygame.display.set_mode([400, 400])
load_screen_splash = pygame.image.load(
    'art/menus/load_screen_splash.png').convert()

load_screen = pygame.display.set_mode([400, 400])
load_screen.blit(load_screen_splash, [0, 0])
pygame.display.flip()


key_color = utilities.colors.key


# ICONS
blockade_runner_icon = pygame.image.load(
    "art/icons/blockade_runner_icon.png").convert_alpha()
blockade_runner_icon.set_colorkey(utilities.colors.key)
blockade_runner_icon = blockade_runner_icon.convert_alpha()
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
fluyt_icon = pygame.image.load('art/icons/galleon_icon.png').convert_alpha()
fluyt_icon.set_colorkey(key_color)
fluyt_icon = fluyt_icon.convert_alpha()
galleon_icon = pygame.image.load("art/icons/galleon_icon.png").convert_alpha()
galleon_icon.set_colorkey(key_color)
galleon_icon = galleon_icon.convert_alpha()

# PORTRAITS
city_portrait_a = pygame.image.load("art/icons/city_a.png").convert_alpha()
city_portrait_b = pygame.image.load("art/icons/city_b.png").convert_alpha()
city_portrait_c = pygame.image.load("art/icons/city_c.png").convert_alpha()
city_portrait_d = pygame.image.load("art/icons/city_d.png").convert_alpha()
city_portraits = [
    city_portrait_a,
    city_portrait_b,
    city_portrait_c,
    city_portrait_d]

shipyard_portrait_img = pygame.image.load("art/icons/shipyard_a.png").convert_alpha()

city_hall_a = pygame.image.load("art/icons/city_hall_a.png")
city_hall_b = pygame.image.load("art/icons/city_hall_b.png")

city_hall_portraits = [city_hall_a,
                       city_hall_b]


# MENUS
port_screen = pygame.image.load("art/menus/port_screen.png").convert()
market_screen = pygame.image.load("art/menus/market_screen.png").convert()
ship_status_screen = pygame.image.load("art/menus/ship_status.png").convert()
quantity_popup = pygame.image.load("art/menus/quantity_popup.png").convert()

mini_map_preview = pygame.image.load("art/menus/mini_map_bg.png").convert()
calendar_menu = pygame.image.load("art/menus/calendar.png").convert()

shipyard_menu = pygame.image.load("art/menus/shipyard_screen.png").convert()

main_menu = pygame.image.load("art/menus/main_menu.png").convert()
options_menu = pygame.image.load("art/menus/options_menu.png").convert()

# RESOURCES
cattle = pygame.image.load("art/resources/cattle_1.png")
cattle.set_colorkey(utilities.colors.key)
cattle = cattle.convert_alpha()

cinnamon = pygame.image.load("art/resources/cinnamon_1.png")
cinnamon.set_colorkey(utilities.colors.key)
cinnamon = cinnamon.convert_alpha()
clove = pygame.image.load("art/resources/clove_1.png")
clove.set_colorkey(utilities.colors.key)
clove = clove.convert_alpha()
fish = pygame.image.load("art/resources/fish.png")
fish.set_colorkey(utilities.colors.key)
fish = fish.convert_alpha()
fruit = pygame.image.load("art/resources/fruit.png")
fruit.set_colorkey(utilities.colors.key)
fruit = fruit.convert_alpha()
gold = pygame.image.load("art/resources/gold_1.png")
gold.set_colorkey(utilities.colors.key)
gold = gold.convert_alpha()
ivory = pygame.image.load("art/resources/ivory_1.png")
ivory.set_colorkey(utilities.colors.key)
ivory = ivory.convert_alpha()
iron = pygame.image.load("art/resources/iron_1.png")
iron.set_colorkey(utilities.colors.key)
iron = iron.convert_alpha()
jewels = pygame.image.load("art/resources/jewels.png")
jewels.set_colorkey(utilities.colors.key)
jewels = jewels.convert_alpha()
pelts = pygame.image.load("art/resources/pelts_1.png")
pelts.set_colorkey(utilities.colors.key)
pelts = pelts.convert_alpha()
saffron = pygame.image.load("art/resources/saffron_1.png")
saffron.set_colorkey(utilities.colors.key)
saffron = saffron.convert_alpha()
shellfish = pygame.image.load("art/resources/shellfish.png")
shellfish.set_colorkey(utilities.colors.key)
shellfish = shellfish.convert_alpha()
silver = pygame.image.load("art/resources/silver_1.png")
silver.set_colorkey(utilities.colors.key)
silver = silver.convert_alpha()
timber = pygame.image.load("art/resources/timber_1.png")
timber.set_colorkey(utilities.colors.key)
timber = timber.convert_alpha()
wheat = pygame.image.load("art/resources/wheat_1.png")
wheat.set_colorkey(utilities.colors.key)
wheat = wheat.convert_alpha()
wool = pygame.image.load("art/resources/wool_1.png")
wool.set_colorkey(utilities.colors.key)
wool = wool.convert_alpha()

resource_images = {"cattle": [cattle],
                   "cinnamon": [cinnamon],
                   "clove": [clove],
                   "fish": [fish],
                   "fruit": [fruit],
                   "gold": [gold],
                   "iron": [iron],
                   "ivory": [ivory],
                   "jewels": [jewels],
                   "pelts": [pelts],
                   "saffron": [saffron],
                   "silver": [silver],
                   "shellfish": [shellfish],
                   "timber": [timber],
                   "wheat": [wheat],
                   "wool": [wool]}


# CONSTRUCTS

city_1 = pygame.image.load("art/constructs/city/ancient_city_1.png")
city_1.set_colorkey(utilities.colors.key)
city_1 = city_1.convert_alpha()
city_2 = pygame.image.load("art/constructs/city/ancient_city_2.png")
city_2.set_colorkey(utilities.colors.key)
city_2 = city_2.convert_alpha()
city_3 = pygame.image.load("art/constructs/city/ancient_city_3.png")
city_3.set_colorkey(utilities.colors.key)
city_3 = city_3.convert_alpha()

# BUILDINGS
city_1 = pygame.image.load("art/constructs/city/ancient_city_1.png").convert_alpha()


# TILES
nw_edge = pygame.image.load("art/tiles/borders/nw.png")
nw_edge.set_colorkey(utilities.colors.key)
nw_edge = nw_edge.convert_alpha()
ne_edge = pygame.image.load("art/tiles/borders/ne.png")
ne_edge.set_colorkey(utilities.colors.key)
ne_edge = ne_edge.convert_alpha()
sw_edge = pygame.image.load("art/tiles/borders/sw.png")
sw_edge.set_colorkey(utilities.colors.key)
sw_edge = sw_edge.convert_alpha()
se_edge = pygame.image.load("art/tiles/borders/se.png")
se_edge.set_colorkey(utilities.colors.key)
se_edge = se_edge.convert_alpha()
border_edges = {(-1, 0): nw_edge,
                (0, -1): ne_edge,
                (0, 1): sw_edge,
                (1, 0): se_edge}

selected_tile_image = pygame.image.load("art/tiles/selected_tile.png")
selected_tile_image.set_colorkey(utilities.colors.key)
selected_tile_image = selected_tile_image.convert_alpha()
grass_tile = pygame.image.load("art/tiles/grassland_1.png")
grass_tile.set_colorkey(utilities.colors.key)
grass_tile = grass_tile.convert_alpha()

ice_tile = pygame.image.load("art/tiles/ice_1.png")
ice_tile.set_colorkey(utilities.colors.key)
ice_tile = ice_tile.convert_alpha()

ocean_tile = pygame.image.load("art/tiles/ocean_1.png")
ocean_tile.set_colorkey(utilities.colors.key)
ocean_tile = ocean_tile.convert_alpha()

sea_tile = pygame.image.load("art/tiles/sea_1.png")
sea_tile.set_colorkey(utilities.colors.key)
sea_tile = sea_tile.convert_alpha()

shallows_tile = pygame.image.load("art/tiles/shallows_1.png")
shallows_tile.set_colorkey(utilities.colors.key)
shallows_tile = shallows_tile.convert_alpha()

river_tile = pygame.image.load("art/tiles/river.png")
river_tile.set_colorkey(utilities.colors.key)
river_tile = river_tile.convert_alpha()

lake_tile = pygame.image.load("art/tiles/lake_1.png")
lake_tile.set_colorkey(utilities.colors.key)
lake_tile = lake_tile.convert_alpha()

tundra_tile = pygame.image.load("art/tiles/tundra_1.png")
tundra_tile.set_colorkey(utilities.colors.key)
tundra_tile = tundra_tile.convert_alpha()

snowy_tundra_tiles_raw = [
    pygame.image.load("art/tiles/snowy_tundra_1.png"),
    pygame.image.load("art/tiles/snowy_tundra_2.png"),
    pygame.image.load("art/tiles/snowy_tundra_3.png")]
snowy_tundra_tiles = []
for each in snowy_tundra_tiles_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snowy_tundra_tiles.append(each)

shrubland_tile = pygame.image.load("art/tiles/shrubland_1.png")
shrubland_tile.set_colorkey(utilities.colors.key)
shrubland_tile = shrubland_tile.convert_alpha()

jungle_tile = pygame.image.load("art/tiles/jungle_1.png")
jungle_tile.set_colorkey(utilities.colors.key)
jungle_tile = jungle_tile.convert_alpha()

forest_tile_1 = pygame.image.load("art/tiles/forest_1.png")
forest_tile_1.set_colorkey(utilities.colors.key)
forest_tile_1 = forest_tile_1.convert_alpha()

grassland_tile = pygame.image.load("art/tiles/grassland_1.png")
grassland_tile.set_colorkey(utilities.colors.key)
grassland_tile = grassland_tile.convert_alpha()

desert_tile = pygame.image.load("art/tiles/desert_1.png")
desert_tile.set_colorkey(utilities.colors.key)
desert_tile = desert_tile.convert_alpha()

plains_tile = pygame.image.load("art/tiles/plains_1.png")
plains_tile.set_colorkey(utilities.colors.key)
plains_tile = plains_tile.convert_alpha()


snowpack_images_raw = [pygame.image.load("art/tiles/snowpack_1.png"),
                       pygame.image.load("art/tiles/snowpack_2.png"),
                       pygame.image.load("art/tiles/snowpack_3.png"),
                       pygame.image.load("art/tiles/snowpack_4.png")]
snowpack_images = []

for each in snowpack_images_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snowpack_images.append(each)

savannah_images_raw = [pygame.image.load("art/tiles/savannah_1.png"),
                       pygame.image.load("art/tiles/savannah_2.png"),
                       pygame.image.load("art/tiles/savannah_3.png")]

savannah_images = []
for each in savannah_images_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    savannah_images.append(each)

desert_images_raw = [pygame.image.load("art/tiles/desert_1.png"),
                     pygame.image.load("art/tiles/desert_2.png"),
                     pygame.image.load("art/tiles/desert_3.png"),
                     pygame.image.load("art/tiles/desert_4.png")]


desert_images = []
for each in desert_images_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    desert_images.append(each)

alpine_images_raw = []
for ii in range(6):
    alpine_images_raw.append(
        pygame.image.load("art/tiles/alpine_{0}.png".format(ii)))

alpine_tiles = []
for each in alpine_images_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    alpine_tiles.append(each)

taiga_images_raw = []
for ii in range(2):
    taiga_images_raw.append(
        pygame.image.load("art/tiles/taiga_{0}.png".format(ii)))

taiga_tiles = []
for each in taiga_images_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    taiga_tiles.append(each)

biome_images = {"grass": [grass_tile],
                "grassland": [grassland_tile],
                "plains": [plains_tile],
                "wet plains": [plains_tile],
                "desert": desert_images,
                "forest": [forest_tile_1],
                "jungle": [jungle_tile],
                "tundra": [tundra_tile],
                "snowy tundra": snowy_tundra_tiles,
                "taiga": taiga_tiles,
                "alpine": alpine_tiles,
                "snowpack": snowpack_images,
                "ice": [ice_tile],
                "savannah": savannah_images,
                "shrubland": [shrubland_tile],
                "ocean": [ocean_tile],
                "sea": [sea_tile],
                "shallows": [shallows_tile],
                "lake": [lake_tile],
                "river": [river_tile]}


# TERRAIN
river_images_raw = []
for ii in range(9):
    river_images_raw.append(
        pygame.image.load('art/tiles/river_{0}.png'.format(ii)))

river_images = []
for img in river_images_raw:
    img.set_colorkey(utilities.colors.key)
    img = img.convert_alpha()
    river_images.append(img)

tree_1 = pygame.image.load("art/constructs/terrain/tree_1.png")
forest_1 = pygame.image.load("art/terrain/forest_1.png")
forest_1.set_colorkey(utilities.colors.key)
forest_1 = forest_1.convert_alpha()
forest_2 = pygame.image.load("art/terrain/forest_2.png")
forest_2.set_colorkey(utilities.colors.key)
forest_2 = forest_2.convert_alpha()

grassland_mountains_raw = []
for ii in range(6):
    grassland_mountains_raw.append(
        pygame.image.load("art/terrain/mountains/grassland_{0}.png".format(ii)))


grassland_mountains = []
for each in grassland_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    grassland_mountains.append(each)

grassland_low_mountains_raw = []
for ii in range(3):
    grassland_low_mountains_raw.append(
        pygame.image.load("art/terrain/low_mountains/grassland_{0}.png".format(ii)))


grassland_low_mountains = []
for each in grassland_low_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    grassland_low_mountains.append(each)


grassland_hills_raw = []
for ii in range(3):
    grassland_hills_raw.append(
        pygame.image.load("art/terrain/hills/grassland_{0}.png".format(ii)))


grassland_hills = []
for each in grassland_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    grassland_hills.append(each)


grassland_low_hills_raw = []
for ii in range(3):
    grassland_low_hills_raw.append(
        pygame.image.load("art/terrain/low_hills/grassland_{0}.png".format(ii)))


grassland_low_hills = []
for each in grassland_low_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    grassland_low_hills.append(each)

grassland_mountains_raw = []
for ii in range(6):
    grassland_mountains_raw.append(
        pygame.image.load("art/terrain/mountains/alpine_{0}.png".format(ii)))

alpine_mountains_raw = []
for ii in range(6):
    alpine_mountains_raw.append(
        pygame.image.load("art/terrain/mountains/alpine_{0}.png".format(ii)))

alpine_mountains = []
for each in alpine_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    alpine_mountains.append(each)

alpine_low_mountains_raw = []
for ii in range(3):
    alpine_low_mountains_raw.append(
        pygame.image.load("art/terrain/low_mountains/alpine_{0}.png".format(ii)))


alpine_low_mountains = []
for each in alpine_low_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    alpine_low_mountains.append(each)


alpine_hills_raw = []
for ii in range(3):
    alpine_hills_raw.append(
        pygame.image.load("art/terrain/hills/alpine_{0}.png".format(ii)))


alpine_hills = []
for each in alpine_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    alpine_hills.append(each)


alpine_low_hills_raw = []
for ii in range(5):
    grassland_low_hills_raw.append(
        pygame.image.load("art/terrain/low_hills/alpine_{0}.png".format(ii)))


alpine_low_hills = []
for each in alpine_low_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    alpine_low_hills.append(each)

tundra_mountains_raw = []
for ii in range(6):
    tundra_mountains_raw.append(
        pygame.image.load("art/terrain/mountains/tundra_{0}.png".format(ii)))

tundra_mountains = []
for each in tundra_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    tundra_mountains.append(each)

tundra_low_mountains_raw = []
for ii in range(3):
    tundra_low_mountains_raw.append(
        pygame.image.load("art/terrain/low_mountains/tundra_{0}.png".format(ii)))


tundra_low_mountains = []
for each in tundra_low_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    tundra_low_mountains.append(each)


tundra_hills_raw = []
for ii in range(3):
    tundra_hills_raw.append(
        pygame.image.load("art/terrain/hills/tundra_{0}.png".format(ii)))


tundra_hills = []
for each in tundra_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    tundra_hills.append(each)


tundra_low_hills_raw = []
for ii in range(3):
    grassland_low_hills_raw.append(
        pygame.image.load("art/terrain/low_hills/tundra_{0}.png".format(ii)))


tundra_low_hills = []
for each in tundra_low_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    tundra_low_hills.append(each)


taiga_mountains_raw = []
for ii in range(6):
    taiga_mountains_raw.append(
        pygame.image.load("art/terrain/mountains/taiga_{0}.png".format(ii)))

taiga_mountains = []
for each in taiga_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    taiga_mountains.append(each)

taiga_low_mountains_raw = []
for ii in range(3):
    taiga_low_mountains_raw.append(
        pygame.image.load("art/terrain/low_mountains/taiga_{0}.png".format(ii)))


taiga_low_mountains = []
for each in taiga_low_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    taiga_low_mountains.append(each)


taiga_hills_raw = []
for ii in range(5):
    taiga_hills_raw.append(
        pygame.image.load("art/terrain/hills/taiga_{0}.png".format(ii)))


taiga_hills = []
for each in taiga_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    taiga_hills.append(each)


snow_mountains_raw = []
for ii in range(6):
    snow_mountains_raw.append(
        pygame.image.load("art/terrain/mountains/snowy_tundra_{0}.png".format(ii)))

snow_mountains = []
for each in snow_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snow_mountains.append(each)


snow_low_mountains_raw = []
for ii in range(3):
    snow_low_mountains_raw.append(
        pygame.image.load("art/terrain/low_mountains/snowy_tundra_{0}.png".format(ii)))


snow_low_mountains = []
for each in snow_low_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snow_low_mountains.append(each)


snow_hills_raw = []
for ii in range(3):
    snow_hills_raw.append(
        pygame.image.load("art/terrain/hills/snowy_tundra_{0}.png".format(ii)))


snow_hills = []
for each in snow_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snow_hills.append(each)

snow_low_hills_raw = []
for ii in range(4):
    snow_low_hills_raw.append(
        pygame.image.load("art/terrain/low_hills/snowy_tundra_{0}.png".format(ii)))

snow_low_hills = []
for each in snow_low_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    snow_low_hills.append(each)

desert_low_hills_raw = []
for ii in range(4):
    desert_low_hills_raw.append(
        pygame.image.load("art/terrain/low_hills/desert_{0}.png".format(ii)))

desert_low_hills = []
for each in desert_low_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    desert_low_hills.append(each)

desert_hills_raw = []
for ii in range(3):
    desert_hills_raw.append(
        pygame.image.load("art/terrain/hills/desert_{0}.png".format(ii)))


desert_hills = []
for each in desert_hills_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    desert_hills.append(each)

desert_low_mountains_raw = []
for ii in range(3):
    desert_low_mountains_raw.append(
        pygame.image.load("art/terrain/low_mountains/desert_{0}.png".format(ii)))


desert_low_mountains = []
for each in desert_low_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    desert_low_mountains.append(each)

desert_mountains_raw = []
for ii in range(6):
    desert_mountains_raw.append(
        pygame.image.load("art/terrain/mountains/desert_{0}.png".format(ii)))

desert_mountains = []
for each in desert_mountains_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    desert_mountains.append(each)

taiga_trees_raw = []
for ii in range(7):
    taiga_trees_raw.append(
        pygame.image.load("art/terrain/taiga_{0}.png".format(ii)))

taiga_trees = []
for each in taiga_trees_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    taiga_trees.append(each)

alpine_trees_raw = []
for ii in range(6):
    alpine_trees_raw.append(
        pygame.image.load("art/terrain/alpine_{0}.png".format(ii)))

alpine_trees = []
for each in alpine_trees_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    alpine_trees.append(each)


wet_plains_trees_raw = []
for ii in range(3):
    wet_plains_trees_raw.append(
        pygame.image.load("art/terrain/wet_plains_trees_{0}.png".format(ii)))


wet_plains_trees = []
for each in wet_plains_trees_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    wet_plains_trees.append(each)

jungle_trees_raw = []
for ii in range(7):
    jungle_trees_raw.append(
        pygame.image.load("art/terrain/jungle_trees_{0}.png".format(ii)))


jungle_trees = []
for each in jungle_trees_raw:
    each.set_colorkey(utilities.colors.key)
    each = each.convert_alpha()
    jungle_trees.append(each)


mountains = {"taiga": taiga_mountains,
             "tundra": tundra_mountains,
             "snowy tundra": tundra_mountains,
             "alpine": alpine_mountains,
             "grassland": taiga_mountains,
             "plains": grassland_mountains,
             "wet plains": grassland_mountains,
             "savannah": desert_mountains,
             "desert": desert_mountains,
             "forest": taiga_mountains,
             "jungle": grassland_mountains,
             "snowpack": snow_mountains,
             "ice": snow_mountains,
             "shrubland": desert_mountains,
             "ocean": grassland_mountains,
             "sea": grassland_mountains,
             "shallows": grassland_mountains,
             "lake": grassland_mountains,
             "river": grassland_mountains}

low_mountains = {"taiga": taiga_low_mountains,
                 "tundra": tundra_low_mountains,
                 "snowy tundra": tundra_low_mountains,
                 "alpine": alpine_low_mountains,
                 "grassland": grassland_low_mountains,
                 "plains": grassland_low_mountains,
                 "wet plains": grassland_low_mountains,
                 "savannah": desert_low_mountains,
                 "desert": desert_low_mountains,
                 "forest": grassland_low_mountains,
                 "jungle": grassland_low_mountains,
                 "snowpack": snow_low_mountains,
                 "ice": snow_low_mountains,
                 "shrubland": desert_low_mountains,
                 "ocean": grassland_low_mountains,
                 "sea": grassland_low_mountains,
                 "shallows": grassland_low_mountains,
                 "lake": grassland_low_mountains,
                 "river": grassland_low_mountains}

hills = {"taiga": taiga_hills,
         "tundra": tundra_hills,
         "snowy tundra": tundra_hills,
         "alpine": alpine_hills,
         "grassland": grassland_hills,
         "plains": grassland_hills,
         "wet plains": grassland_hills,
         "savannah": desert_hills,
         "desert": desert_hills,
         "forest": grassland_hills,
         "jungle": grassland_hills,
         "snowpack": snow_hills,
         "ice": snow_hills,
         "shrubland": desert_hills,
         "ocean": grassland_hills,
         "sea": grassland_hills,
         "shallows": grassland_hills,
         "lake": grassland_hills,
         "river": grassland_hills}

low_hills = {"taiga": grassland_low_hills,
             "tundra": tundra_low_hills,
             "alpine": alpine_low_hills,
             "snowy tundra": tundra_low_hills,
             "grassland": grassland_low_hills,
             "plains": grassland_low_hills,
             "wet plains": grassland_low_hills,
             "savannah": desert_low_hills,
             "desert": desert_low_hills,
             "forest": grassland_low_hills,
             "jungle": grassland_low_hills,
             "snowpack": snow_low_hills,
             "ice": snow_low_hills,
             "shrubland": desert_low_hills,
             "ocean": grassland_low_hills,
             "sea": grassland_low_hills,
             "shallows": grassland_low_hills,
             "lake": grassland_low_hills,
             "river": grassland_low_hills}


vegetation = {"taiga": taiga_trees,
              "tundra": None,
              "snowy tundra": None,
              "alpine": alpine_trees,
              "grassland": None,
              "plains": None,
              "wet plains": wet_plains_trees,
              "savannah": None,
              "desert": None,
              "forest": [forest_1, forest_2],
              "jungle": jungle_trees,
              "snowpack": None,
              "ice": None,
              "shrubland": None,
              "ocean": None,
              "sea": None,
              "shallows": None,
              "lake": None,
              "river": None}

terrain_images = {"mountain": mountains,
                  "low mountain": low_mountains,
                  "hill": hills,
                  "low hill": low_hills,
"vegetation": vegetation}