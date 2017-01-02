import pygame
import utilities


pygame.init()
pygame.display.set_mode([0, 0])

map_image = pygame.image.load("world_map.png").convert()
port_layer_width = map_image.get_width()
port_layer_height = map_image.get_height()
port_layer = pygame.Surface([port_layer_width, port_layer_height])
key_color = (255, 0, 128)
port_layer.fill(key_color)
port_marker = pygame.image.load("port_marker.png").convert()
date_bar = pygame.image.load("date_bar.png").convert()


#ICONS
galleon_icon = pygame.image.load("assets/art/galleon_icon.png").convert_alpha()
port_icon = pygame.image.load("assets/art/port_icon.png").convert_alpha()


#BUTTONS
x_regular = pygame.image.load("assets/art/buttons/x_regular.png").convert_alpha()
x_hover = pygame.image.load("assets/art/buttons/x_hover.png").convert_alpha()

market_regular = pygame.image.load("assets/art/buttons/market_regular.png").convert_alpha()
market_hover = pygame.image.load("assets/art/buttons/market_hover.png").convert_alpha()

arrow_down_regular = pygame.image.load("assets/art/buttons/arrow_down_regular.png").convert_alpha()
arrow_down_hover = pygame.image.load("assets/art/buttons/arrow_down_hover.png").convert_alpha()

arrow_up_regular = pygame.image.load("assets/art/buttons/arrow_up_regular.png").convert_alpha()
arrow_up_hover = pygame.image.load("assets/art/buttons/arrow_up_hover.png").convert_alpha()

arrow_left_regular = pygame.image.load("assets/art/buttons/arrow_left_regular.png").convert_alpha()
arrow_left_hover = pygame.image.load("assets/art/buttons/arrow_left_hover.png").convert_alpha()

arrow_right_regular = pygame.image.load("assets/art/buttons/arrow_right_regular.png").convert_alpha()
arrow_right_hover = pygame.image.load("assets/art/buttons/arrow_right_hover.png").convert_alpha()

buy_regular = pygame.image.load("assets/art/buttons/buy_regular.png").convert_alpha()
buy_hover = pygame.image.load("assets/art/buttons/buy_hover.png").convert_alpha()

sell_regular = pygame.image.load("assets/art/buttons/sell_regular.png").convert_alpha()
sell_hover = pygame.image.load("assets/art/buttons/sell_hover.png").convert_alpha()

done_regular = pygame.image.load("assets/art/buttons/done_regular.png").convert_alpha()
done_hover = pygame.image.load("assets/art/buttons/done_hover.png").convert_alpha()

view_port_regular = pygame.image.load("assets/art/buttons/view_port_regular.png").convert_alpha()
view_port_hover = pygame.image.load("assets/art/buttons/view_port_hover.png").convert_alpha()

goto_regular = pygame.image.load("assets/art/buttons/goto_regular.png").convert_alpha()
goto_hover = pygame.image.load("assets/art/buttons/goto_hover.png").convert_alpha()

#MENUS
port_screen = pygame.image.load("assets/art/menus/port_screen.png").convert_alpha()
market_screen = pygame.image.load("assets/art/menus/market_screen.png").convert_alpha()
ship_status_screen = pygame.image.load("assets/art/menus/ship_status_screen.png").convert_alpha()