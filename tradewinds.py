import pygame
import calendar
import port
import assets
import ui
import utilities
import ships


pygame.init()
pygame.display.set_mode([0, 0])

screen_width = 950
screen_height = 800

fps_cap = 60


class Player(object):
    def __init__(self):
        self.ship = None
        self.silver = 0


class GameState(object):
    def __init__(self):
        self.player = None
        self.ports = {}
        self.current_day = 0
        self.current_month = 0
        self.current_year = 0
        self.port_layer = None

    def get_date_string(self):
        date_string = "{0} {1} {2}".format(self.current_month,
                                           self.current_day,
                                           self.current_year)
        return date_string

    def advance_date(self):
        self.current_day += 1
        if self.current_day + 1 > calendar.days_per_month[self.current_month]:
            self.current_day = 1
            if self.current_month != "December":
                self.current_month = calendar.months[calendar.months.index(self.current_month) + 1]
            else:
                self.current_month = "January"
                self.current_year += 1

    def randomize_port_commodities(self):
        for key, value in self.ports.items():
            value.set_random_supply()


def day_loop():
    pass


def update_port_layer(port_layer, list_of_ports):
    port_layer.fill(assets.key_color)
    for each in list_of_ports:
        port_layer.blit(assets.port_marker, [list_of_ports[each].x, list_of_ports[each].y])
    port_layer.set_colorkey(assets.key_color)
    print("Updated port layer")


def assign_spaces(new_ports, screen, scroll_x, scroll_y, game_state):
    for each in new_ports:
        not_placed = True
        print(each)
        while not_placed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        x = mouse_pos[0] - scroll_x - 5
                        y = mouse_pos[1] - scroll_y - 5
                        game_state.ports[each] = (x, y)
                        update_port_layer(game_state.port_layer, game_state.ports)
                        print("placed")
                        not_placed = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        scroll_x -= 10
                        draw_to_screen(screen, scroll_x, scroll_y, game_state)
                    elif event.key == pygame.K_LEFT:
                        scroll_x += 10
                        draw_to_screen(screen, scroll_x, scroll_y, game_state)
                    elif event.key == pygame.K_UP:
                        scroll_y += 10
                        draw_to_screen(screen, scroll_x, scroll_y, game_state)
                    elif event.key == pygame.K_DOWN:
                        scroll_y -= 10
                        draw_to_screen(screen, scroll_x, scroll_y, game_state)
        draw_to_screen(screen, scroll_x, scroll_y, game_state)


def print_list_of_ports(list_of_ports):
    for each_port in list_of_ports:
        print(each_port, list_of_ports[each_port])


def draw_to_screen(screen, scroll_x, scroll_y, game_state):
    font = pygame.font.SysFont('Calibri', 14, True, False)
    screen.fill((0, 0, 255))
    screen.blit(assets.map_image, [scroll_x, scroll_y])
    screen.blit(game_state.port_layer, [scroll_x, scroll_y])
    screen.blit(assets.date_bar, [0, 0])
    date_stamp = font.render(game_state.get_date_string(), True, (0, 0, 0))
    screen.blit(date_stamp, [7, 7])
    silver_stamp = font.render("$ {0}".format(str(game_state.player.silver)), True, (0, 0, 0))
    screen.blit(silver_stamp, [130, 7])
    screen.blit(assets.ship_icon, [game_state.player.ship.x + scroll_x,
                                   game_state.player.ship.y + scroll_y])
    pygame.display.flip()


def new_game():
    new_game = GameState()
    new_game.player = Player()
    port_layer_width = assets.map_image.get_width()
    port_layer_height = assets.map_image.get_height()
    new_game.port_layer = pygame.Surface([port_layer_width, port_layer_height])
    new_game.current_year = 1600
    new_game.current_month = "January"
    new_game.current_day = 1
    new_game.player.silver = 100
    new_game.player.ship = ships.Cog()
    new_game.player.ship.cargo["Pepper"] = 10

    for port_name in port.port_coordinates:
        new_port_x = port.port_coordinates[port_name][0]
        new_port_y = port.port_coordinates[port_name][1]
        new_game.ports[port_name] = port.Port(port_name,
                                              new_port_x,
                                              new_port_y)
    new_game.randomize_port_commodities()
    update_port_layer(new_game.port_layer, new_game.ports)
    return new_game


def main():
    game_state = new_game()
    clock = pygame.time.Clock()
    playing = True
    scroll_x = -1060
    scroll_y = -60
    game_speed = 100
    """5 is Llama speed, 10 is fast, 100 is normal, 200 is slow, 400 is very slow"""
    day_timer = 0
    screen = pygame.display.set_mode([screen_width, screen_height])
    while playing:
        date = game_state.get_date_string()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    playing = False
                elif event.key == pygame.K_p:
                    assign_spaces(screen, scroll_x, scroll_y, date, game_state.player)
                elif event.key == pygame.K_c:
                    print_list_of_ports(game_state.ports)
                elif event.key == pygame.K_RIGHT:
                    scroll_x -= 10
                elif event.key == pygame.K_LEFT:
                    scroll_x += 10
                elif event.key == pygame.K_UP:
                    scroll_y += 10
                elif event.key == pygame.K_DOWN:
                    scroll_y -= 10
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for key, value in game_state.ports.items():
                    if utilities.check_if_inside(value.x + scroll_x,
                                                 value.x + scroll_x + 10,
                                                 value.y + scroll_y,
                                                 value.y + scroll_y + 10,
                                                 pos):
                        game_state.player.ship.x = value.x
                        game_state.player.ship.y = value.y
                        draw_to_screen(screen, scroll_x, scroll_y, game_state)
                        port_menu = ui.PortMenu(screen,
                                                game_state.player,
                                                value)
                        port_menu.menu_onscreen()
        draw_to_screen(screen, scroll_x, scroll_y, game_state)
        day_timer += 1
        if day_timer >= game_speed:
            day_timer = 0
            day_loop()
            game_state.advance_date()
        clock.tick(fps_cap)



main()
