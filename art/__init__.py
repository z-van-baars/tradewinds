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
city_portrait_a = pygame.image.load("art/icons/city_a.png").convert()
city_portrait_b = pygame.image.load("art/icons/city_b.png").convert()
city_portrait_c = pygame.image.load("art/icons/city_c.png").convert()
city_portrait_d = pygame.image.load("art/icons/city_d.png").convert()
city_portraits = [
    city_portrait_a,
    city_portrait_b,
    city_portrait_c,
    city_portrait_d]

shipyard_portrait_img = pygame.image.load("art/icons/shipyard_a.png").convert()

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
resource_images = {}
for name in [
        "cattle",
        "cinnamon",
        "clove",
        "fish",
        "fruit",
        "gold",
        "iron",
        "ivory",
        "jewels",
        "pelts",
        "saffron",
        "silver",
        "shellfish",
        "timber",
        "wheat",
        "wool"]:
    resource_images[name] = [pygame.image.load(
        "art/resources/{0}_1.png".format(name))]

for key, img_list in resource_images.items():
    for each_img in img_list:
        each_img.set_colorkey(utilities.colors.key)
        each_img = each_img.convert_alpha()


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
ne_edge = pygame.image.load("art/tiles/borders/ne.png")
sw_edge = pygame.image.load("art/tiles/borders/sw.png")
se_edge = pygame.image.load("art/tiles/borders/se.png")
border_edges = {(-1, 0): nw_edge,
                (0, -1): ne_edge,
                (0, 1): sw_edge,
                (1, 0): se_edge}

for edge_xy, edge_img in border_edges.items():
    edge_img.set_colorkey(utilities.colors.key)
    edge_img = edge_img.convert_alpha()

selected_tile_image = pygame.image.load("art/tiles/selected_tile.png")
selected_tile_image.set_colorkey(utilities.colors.key)
selected_tile_image = selected_tile_image.convert_alpha()


grass_tile = pygame.image.load("art/tiles/grassland_1.png")
ice_tile = pygame.image.load("art/tiles/ice_1.png")
ocean_tile = pygame.image.load("art/tiles/ocean_1.png")
sea_tile = pygame.image.load("art/tiles/sea_1.png")
shallows_tile = pygame.image.load("art/tiles/shallows_1.png")
lake_tile = pygame.image.load("art/tiles/lake_1.png")
tundra_tile = pygame.image.load("art/tiles/tundra_1.png")

snowy_tundra_tiles = [
    pygame.image.load("art/tiles/snowy_tundra_1.png"),
    pygame.image.load("art/tiles/snowy_tundra_2.png"),
    pygame.image.load("art/tiles/snowy_tundra_3.png")]

shrubland_tile = pygame.image.load("art/tiles/shrubland_1.png")
jungle_tile = pygame.image.load("art/tiles/jungle_1.png")
forest_tile_1 = pygame.image.load("art/tiles/forest_1.png")
grassland_tile = pygame.image.load("art/tiles/grassland_1.png")
plains_tile = pygame.image.load("art/tiles/plains_1.png")

snowpack_tiles = [pygame.image.load("art/tiles/snowpack_1.png"),
                  pygame.image.load("art/tiles/snowpack_2.png"),
                  pygame.image.load("art/tiles/snowpack_3.png"),
                  pygame.image.load("art/tiles/snowpack_4.png")]
savannah_tiles = [pygame.image.load("art/tiles/savannah_1.png"),
                  pygame.image.load("art/tiles/savannah_2.png"),
                  pygame.image.load("art/tiles/savannah_3.png")]
desert_tiles = [pygame.image.load("art/tiles/desert_1.png"),
                pygame.image.load("art/tiles/desert_2.png"),
                pygame.image.load("art/tiles/desert_3.png"),
                pygame.image.load("art/tiles/desert_4.png")]

alpine_tiles = []
for ii in range(6):
    alpine_tiles.append(
        pygame.image.load("art/tiles/alpine_{0}.png".format(ii)))

taiga_tiles = []
for ii in range(2):
    taiga_tiles.append(
        pygame.image.load("art/tiles/taiga_{0}.png".format(ii)))

biome_images = {"grass": [grass_tile],
                "grassland": [grassland_tile],
                "plains": [plains_tile],
                "wet plains": [plains_tile],
                "desert": desert_tiles,
                "forest": [forest_tile_1],
                "jungle": [jungle_tile],
                "tundra": [tundra_tile],
                "snowy tundra": snowy_tundra_tiles,
                "taiga": taiga_tiles,
                "alpine": alpine_tiles,
                "snowpack": snowpack_tiles,
                "ice": [ice_tile],
                "savannah": savannah_tiles,
                "shrubland": [shrubland_tile],
                "ocean": [ocean_tile],
                "sea": [sea_tile],
                "shallows": [shallows_tile],
                "lake": [lake_tile]}

for biome_name, img_list in biome_images.items():
    for img_file in img_list:
        img_file.set_colorkey(utilities.colors.key)
        img_file = img_file.convert_alpha()

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

grassland_mountains = []
for ii in range(6):
    grassland_mountains.append(pygame.image.load(
        "art/terrain/mountains/grassland_{0}.png".format(ii)))
grassland_low_mountains = []
for ii in range(3):
    grassland_low_mountains.append(
        pygame.image.load("art/terrain/low_mountains/grassland_{0}.png".format(ii)))
grassland_hills = []
for ii in range(3):
    grassland_hills.append(
        pygame.image.load("art/terrain/hills/grassland_{0}.png".format(ii)))
grassland_low_hills = []
for ii in range(3):
    grassland_low_hills.append(
        pygame.image.load("art/terrain/low_hills/grassland_{0}.png".format(ii)))

alpine_mountains = []
for ii in range(6):
    alpine_mountains.append(
        pygame.image.load("art/terrain/mountains/alpine_{0}.png".format(ii)))
alpine_low_mountains = []
for ii in range(3):
    alpine_low_mountains.append(
        pygame.image.load("art/terrain/low_mountains/alpine_{0}.png".format(ii)))
alpine_hills = []
for ii in range(4):
    alpine_hills.append(
        pygame.image.load("art/terrain/hills/alpine_{0}.png".format(ii)))
alpine_low_hills = []
for ii in range(4):
    alpine_low_hills.append(
        pygame.image.load("art/terrain/low_hills/alpine_{0}.png".format(ii)))

tundra_mountains = []
for ii in range(6):
    tundra_mountains.append(
        pygame.image.load("art/terrain/mountains/tundra_{0}.png".format(ii)))
tundra_low_mountains = []
for ii in range(3):
    tundra_low_mountains.append(
        pygame.image.load("art/terrain/low_mountains/tundra_{0}.png".format(ii)))
tundra_hills = []
for ii in range(3):
    tundra_hills.append(
        pygame.image.load("art/terrain/hills/tundra_{0}.png".format(ii)))
tundra_low_hills = []
for ii in range(3):
    tundra_low_hills.append(
        pygame.image.load("art/terrain/low_hills/tundra_{0}.png".format(ii)))

taiga_mountains = []
for ii in range(6):
    taiga_mountains.append(
        pygame.image.load("art/terrain/mountains/taiga_{0}.png".format(ii)))
taiga_low_mountains = []
for ii in range(3):
    taiga_low_mountains.append(
        pygame.image.load("art/terrain/low_mountains/taiga_{0}.png".format(ii)))
taiga_hills = []
for ii in range(5):
    taiga_hills.append(
        pygame.image.load("art/terrain/hills/taiga_{0}.png".format(ii)))

snow_mountains = []
for ii in range(6):
    snow_mountains.append(
        pygame.image.load("art/terrain/mountains/snowy_tundra_{0}.png".format(ii)))
snow_low_mountains = []
for ii in range(3):
    snow_low_mountains.append(
        pygame.image.load("art/terrain/low_mountains/snowy_tundra_{0}.png".format(ii)))
snow_hills = []
for ii in range(3):
    snow_hills.append(
        pygame.image.load("art/terrain/hills/snowy_tundra_{0}.png".format(ii)))
snow_low_hills = []
for ii in range(4):
    snow_low_hills.append(
        pygame.image.load("art/terrain/low_hills/snowy_tundra_{0}.png".format(ii)))

desert_low_hills = []
for ii in range(4):
    desert_low_hills.append(
        pygame.image.load("art/terrain/low_hills/desert_{0}.png".format(ii)))
desert_hills = []
for ii in range(3):
    desert_hills.append(
        pygame.image.load("art/terrain/hills/desert_{0}.png".format(ii)))
desert_low_mountains = []
for ii in range(3):
    desert_low_mountains.append(
        pygame.image.load("art/terrain/low_mountains/desert_{0}.png".format(ii)))
desert_mountains = []
for ii in range(6):
    desert_mountains.append(
        pygame.image.load("art/terrain/mountains/desert_{0}.png".format(ii)))

savannah_low_hills = []
for ii in range(4):
    savannah_low_hills.append(
        pygame.image.load("art/terrain/low_hills/savannah_{0}.png".format(ii)))
savannah_hills = []
for ii in range(3):
    savannah_hills.append(
        pygame.image.load("art/terrain/hills/savannah_{0}.png".format(ii)))
savannah_low_mountains = []
for ii in range(3):
    savannah_low_mountains.append(
        pygame.image.load("art/terrain/low_mountains/savannah_{0}.png".format(ii)))
savannah_mountains = []
for ii in range(6):
    savannah_mountains.append(
        pygame.image.load("art/terrain/mountains/savannah_{0}.png".format(ii)))

plains_low_hills = []
for ii in range(4):
    plains_low_hills.append(
        pygame.image.load("art/terrain/low_hills/plains_{0}.png".format(ii)))
plains_hills = []
for ii in range(3):
    plains_hills.append(
        pygame.image.load("art/terrain/hills/plains_{0}.png".format(ii)))
plains_low_mountains = []
for ii in range(3):
    plains_low_mountains.append(
        pygame.image.load("art/terrain/low_mountains/plains_{0}.png".format(ii)))
plains_mountains = []
for ii in range(6):
    plains_mountains.append(
        pygame.image.load("art/terrain/mountains/plains_{0}.png".format(ii)))

taiga_trees = []
for ii in range(7):
    taiga_trees.append(
        pygame.image.load("art/terrain/taiga_{0}.png".format(ii)))

alpine_trees = []
for ii in range(6):
    alpine_trees.append(
        pygame.image.load("art/terrain/alpine_{0}.png".format(ii)))

wet_plains_trees = []
for ii in range(3):
    wet_plains_trees.append(
        pygame.image.load("art/terrain/wet_plains_trees_{0}.png".format(ii)))

jungle_trees = []
for ii in range(7):
    jungle_trees.append(
        pygame.image.load("art/terrain/jungle_trees_{0}.png".format(ii)))


mountains = {"taiga": taiga_mountains,
             "tundra": tundra_mountains,
             "snowy tundra": tundra_mountains,
             "alpine": alpine_mountains,
             "grassland": taiga_mountains,
             "plains": plains_mountains,
             "wet plains": plains_mountains,
             "savannah": savannah_mountains,
             "desert": desert_mountains,
             "forest": taiga_mountains,
             "jungle": grassland_mountains,
             "snowpack": snow_mountains,
             "ice": snow_mountains,
             "shrubland": plains_mountains,
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
                 "plains": plains_low_mountains,
                 "wet plains": plains_low_mountains,
                 "savannah": savannah_low_mountains,
                 "desert": desert_low_mountains,
                 "forest": grassland_low_mountains,
                 "jungle": grassland_low_mountains,
                 "snowpack": snow_low_mountains,
                 "ice": snow_low_mountains,
                 "shrubland": plains_low_mountains,
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
         "plains": plains_hills,
         "wet plains": plains_hills,
         "savannah": savannah_hills,
         "desert": desert_low_hills,
         "forest": grassland_hills,
         "jungle": grassland_hills,
         "snowpack": snow_hills,
         "ice": snow_hills,
         "shrubland": plains_hills,
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
             "plains": plains_low_hills,
             "wet plains": plains_low_hills,
             "savannah": savannah_low_hills,
             "desert": desert_low_hills,
             "forest": grassland_low_hills,
             "jungle": grassland_low_hills,
             "snowpack": snow_low_hills,
             "ice": snow_low_hills,
             "shrubland": plains_low_hills,
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
              "lake": None}

terrain_images = {"mountain": mountains,
                  "low mountain": low_mountains,
                  "hill": hills,
                  "low hill": low_hills,
                  "vegetation": vegetation}


for terrain_type, t_dict in terrain_images.items():
    for biome_name, img_list in t_dict.items():
        if img_list is None:
            continue
        for img in img_list:
            img.set_colorkey(utilities.colors.key)
            img = img.convert_alpha()
