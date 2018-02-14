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


# TILES
grass_tile = pygame.image.load("art/tiles/grassland_1.png").convert_alpha()
grass_tile.set_colorkey(utilities.colors.key)
grass_tile = grass_tile.convert_alpha()
ocean_tile = pygame.image.load("art/tiles/ocean_1.png").convert_alpha()
ocean_tile.set_colorkey(utilities.colors.key)
ocean_tile = ocean_tile.convert_alpha()
tundra_tile = pygame.image.load("art/tiles/tundra_1.png").convert_alpha()
tundra_tile.set_colorkey(utilities.colors.key)
tundra_tile = tundra_tile.convert_alpha()
grassland_tile = pygame.image.load("art/tiles/grassland_1.png").convert_alpha()
grassland_tile.set_colorkey(utilities.colors.key)
grassland_tile = grassland_tile.convert_alpha()
desert_tile = pygame.image.load("art/tiles/desert_1.png").convert_alpha()
desert_tile.set_colorkey(utilities.colors.key)
desert_tile = desert_tile.convert_alpha()
plains_tile = pygame.image.load("art/tiles/plains_1.png").convert_alpha()
plains_tile.set_colorkey(utilities.colors.key)
plains_tile = plains_tile.convert_alpha()
ice_tile = pygame.image.load("art/tiles/ice_1.png").convert_alpha()
ice_tile.set_colorkey(utilities.colors.key)
ice_tile = ice_tile.convert_alpha()


# TERRAIN
tree_1 = pygame.image.load("art/constructs/terrain/tree_1.png").convert_alpha()
forest_1 = pygame.image.load("art/terrain/forest_1.png").convert_alpha()
mountain_1 = pygame.image.load("art/terrain/mountain_1.png").convert_alpha()
mountain_1.set_colorkey(utilities.colors.key)
mountain_1 = mountain_1.convert_alpha()
hill_1 = pygame.image.load("art/terrain/hill_1.png").convert_alpha()
hill_1.set_colorkey(utilities.colors.key)
hill_1 = hill_1.convert_alpha()

# BUILDINGS
city_1 = pygame.image.load("art/constructs/city/ancient_city_1.png").convert_alpha()

biome_images = {"grass": grass_tile,
                "grassland": grassland_tile,
                "plains": plains_tile,
                "desert": desert_tile,
                "tundra": tundra_tile,
                "taiga": tundra_tile,
                "ice": ice_tile,
                "ocean": ocean_tile}

terrain_images = {"mountain": mountain_1,
                  "hill": hill_1}
