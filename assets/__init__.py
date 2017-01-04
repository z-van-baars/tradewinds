import pygame
import utilities


pygame.init()
pygame.display.set_mode([0, 0])

map_image = pygame.image.load("assets/art/world_map.png").convert()
key_color = (255, 0, 128)
date_bar = pygame.image.load("assets/art/date_bar.png").convert()


#ICONS
galleon_icon = pygame.image.load("assets/art/galleon_icon.png").convert_alpha()
port_marker = pygame.image.load("assets/art/port_marker.png").convert_alpha()
node_marker = pygame.image.load("assets/art/node_marker.png").convert_alpha()
node_marker.set_colorkey(key_color)
node_marker = node_marker.convert_alpha()
selected_node_icon = pygame.image.load("assets/art/selected_node_icon.png").convert_alpha()
selected_node_icon.set_colorkey(key_color)
selected_node_icon = selected_node_icon.convert_alpha()
ship_icon = pygame.image.load("assets/art/ship_icon.png").convert_alpha()
ship_icon.set_colorkey(key_color)
ship_icon = ship_icon.convert_alpha()


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

cancel_regular = pygame.image.load("assets/art/buttons/cancel_regular.png").convert_alpha()
cancel_hover = pygame.image.load("assets/art/buttons/cancel_hover.png").convert_alpha()

view_port_regular = pygame.image.load("assets/art/buttons/view_port_regular.png").convert_alpha()
view_port_hover = pygame.image.load("assets/art/buttons/view_port_hover.png").convert_alpha()

goto_regular = pygame.image.load("assets/art/buttons/goto_regular.png").convert_alpha()
goto_hover = pygame.image.load("assets/art/buttons/goto_hover.png").convert_alpha()

repair_regular = pygame.image.load("assets/art/buttons/repair_regular.png").convert_alpha()
repair_hover = pygame.image.load("assets/art/buttons/repair_hover.png").convert_alpha()

#MENUS
port_screen = pygame.image.load("assets/art/menus/port_screen.png").convert_alpha()
market_screen = pygame.image.load("assets/art/menus/market_screen.png").convert_alpha()
ship_status_screen = pygame.image.load("assets/art/menus/ship_status.png").convert_alpha()
quantity_popup = pygame.image.load("assets/art/menus/quantity_popup.png").convert_alpha()