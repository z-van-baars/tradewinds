import pygame
import calendar
import port
import assets
import ui
import utilities
import ships
import navigate


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
        self.node_layer = None
        self.nav_edge_layer = None
        self.nav_nodes = {}
        self.nav_edges = {}

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

    def randomize_port_demand(self):
        for each_id, each_port in self.ports.items():
            each_port.set_demand_for_spices()


def day_loop():
    pass


def update_port_layer(port_layer, list_of_ports):
    port_layer.fill(assets.key_color)
    for each in list_of_ports:
        port_layer.blit(assets.port_marker, [list_of_ports[each].x, list_of_ports[each].y])
    port_layer.set_colorkey(assets.key_color)
    port_layer = port_layer.convert_alpha()
    print("Updated port layer")


def update_node_layer(node_layer, list_of_nodes):
    node_layer.fill(assets.key_color)
    for each in list_of_nodes:
        node_layer.blit(assets.node_marker, [list_of_nodes[each].x - 3, list_of_nodes[each].y - 3])
    node_layer.set_colorkey(assets.key_color)
    node_layer = node_layer.convert_alpha()
    print("Updated node layer")


def update_nav_edge_layer(nav_edge_layer, list_of_edges):
    nav_edge_layer.fill(assets.key_color)
    small_font = pygame.font.SysFont("Calibri", 10, True, False)
    for each_id, each_edge in list_of_edges.items():
        pygame.draw.line(nav_edge_layer,
                         (255, 40, 40),
                         (each_edge.points[0].x, each_edge.points[0].y),
                         (each_edge.points[1].x, each_edge.points[1].y))
    nav_edge_layer.set_colorkey(assets.key_color)
    # nav_edge_layer = nav_edge_layer.convert_alpha()

    for each_id, each_edge in list_of_edges.items():
        cost_stamp = small_font.render(str(each_edge.cost), True, (255, 255, 255))
        backing = pygame.Surface([cost_stamp.get_width(), cost_stamp.get_height()])
        backing.fill((36, 92, 104))
        x_dist = each_edge.x - each_edge.a
        y_dist = each_edge.y - each_edge.b
        cost_x = each_edge.x - (x_dist / 2)
        cost_y = each_edge.y - (y_dist / 2)
        backing.blit(cost_stamp, [0, 0])
        backing.set_colorkey((36, 92, 104))
        nav_edge_layer.blit(backing, [cost_x, cost_y])
    # nav_edge_layer = nav_edge_layer.convert_alpha()


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
                    scroll_x, scroll_y = scroll_handler(event, scroll_x, scroll_y)
        draw_to_screen(screen, scroll_x, scroll_y, game_state)


def print_list_of_ports(list_of_ports):
    for each_port in list_of_ports:
        print(each_port, list_of_ports[each_port])


def draw_to_screen(screen, scroll_x, scroll_y, game_state, placing_nodes=False, adding_neighbors=False, selected_node=None):
    font = pygame.font.SysFont('Calibri', 14, True, False)
    header_font = pygame.font.SysFont("Calibri", 18, True, False)
    add_neighbors_stamp = header_font.render("RC to add a neighbor, LC to finish", True, (255, 255, 255))
    node_placement_stamp = header_font.render("RC to place, LC to edit neighbors", True, (255, 255, 255))

    screen.fill((0, 0, 255))
    screen.blit(assets.map_image, [scroll_x, scroll_y])
    screen.blit(game_state.port_layer, [scroll_x, scroll_y])
    screen.blit(game_state.node_layer, [scroll_x, scroll_y])
    screen.blit(assets.date_bar, [0, 0])
    date_stamp = font.render(game_state.get_date_string(), True, (0, 0, 0))
    screen.blit(date_stamp, [7, 7])
    silver_stamp = font.render("$ {0}".format(str(game_state.player.silver)), True, (0, 0, 0))
    screen.blit(silver_stamp, [130, 7])
    screen.blit(assets.ship_icon, [game_state.player.ship.x + scroll_x,
                                   game_state.player.ship.y + scroll_y])
    if placing_nodes:
        screen.blit(node_placement_stamp, [300, 10])
    if adding_neighbors:
        screen.blit(add_neighbors_stamp, [300, 10])
        screen.blit(game_state.nav_edge_layer, [scroll_x, scroll_y])
        if selected_node:
            screen.blit(assets.selected_node_icon, [selected_node.x - 3 + scroll_x, selected_node.y - 3 + scroll_y])
    pygame.display.flip()


def scroll_handler(event, scroll_x, scroll_y):
    if event.key == pygame.K_RIGHT:
        scroll_x -= 10
    elif event.key == pygame.K_LEFT:
        scroll_x += 10
    elif event.key == pygame.K_UP:
        scroll_y += 10
    elif event.key == pygame.K_DOWN:
        scroll_y -= 10
    return scroll_x, scroll_y


def add_neighbors(screen, scroll_x, scroll_y, game_state, selected_node):
    print("adding neighbors to {0}".format(id(selected_node)))
    adding_neighbors = True
    while adding_neighbors:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.display.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_xy = pygame.mouse.get_pos()
                mouse_x = mouse_xy[0] - scroll_x
                mouse_y = mouse_xy[1] - scroll_y
                if event.button == 3:
                    new_neighbor_id = None
                    for each_id, each_node in game_state.nav_nodes.items():
                        if utilities.check_if_inside(each_node.x - 6,
                                                     each_node.x + 6,
                                                     each_node.y - 6,
                                                     each_node.y + 6,
                                                     (mouse_x, mouse_y)):
                            new_neighbor_id = each_id
                            break
                    if new_neighbor_id:
                        print("adding neighbor {0}".format(new_neighbor_id))
                        if new_neighbor_id not in selected_node.neighbors:
                            selected_node.neighbors.append(new_neighbor_id)
                            neighbor_x, neighbor_y = game_state.nav_nodes[new_neighbor_id].x, game_state.nav_nodes[new_neighbor_id].y
                            new_edge = navigate.MapEdge(selected_node.x,
                                                        selected_node.y,
                                                        neighbor_x,
                                                        neighbor_y)
                            new_edge.points.append(selected_node)
                            new_edge.points.append(game_state.nav_nodes[new_neighbor_id])
                            raw_cost = utilities.distance(new_edge.x, new_edge.y, new_edge.a, new_edge.b)
                            raw_cost = round(raw_cost / 10) + 1
                            new_edge.cost = raw_cost
                            duplicate_edge = False
                            for each_id, each_edge in game_state.nav_edges.items():
                                point_a = each_edge.points[0]
                                point_b = each_edge.points[1]
                                if point_a == selected_node and point_b == game_state.nav_nodes[new_neighbor_id]:
                                    print("this connection already exists!")
                                    duplicate_edge = True
                                    break
                                elif point_a == game_state.nav_nodes[new_neighbor_id] and point_b == selected_node:
                                    print("this connection already exists!")
                                    duplicate_edge = True
                                    break
                            if not duplicate_edge:
                                print("added an edge!")
                                game_state.nav_edges[id(new_edge)] = new_edge
                                update_node_layer(game_state.node_layer, game_state.nav_nodes)
                                update_nav_edge_layer(game_state.nav_edge_layer, game_state.nav_edges)
                        else:
                            print("this connection already exists!")

                elif event.button == 1:
                    selected_node = None
                    adding_neighbors = False

            elif event.type == pygame.KEYDOWN:
                scroll_x, scroll_y = scroll_handler(event, scroll_x, scroll_y)
                if event.key == pygame.K_d:
                    node_to_delete = id(selected_node)
                    adding_neighbors = False
                    return node_to_delete
        draw_to_screen(screen, scroll_x, scroll_y, game_state, False, True, selected_node)
        pygame.display.flip()
    return None


def place_nodes(screen, scroll_x, scroll_y, game_state):
    placing_nodes = True
    print("placing nodes")
    selected_node = None
    while placing_nodes:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.display.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_xy = pygame.mouse.get_pos()
                mouse_x = mouse_xy[0] - scroll_x
                mouse_y = mouse_xy[1] - scroll_y
                if event.button == 3:
                    selected_node = None
                    new_node = navigate.MapNode(mouse_x, mouse_y, True)
                    new_node_id = id(new_node)
                    game_state.nav_nodes[new_node_id] = new_node
                    update_node_layer(game_state.node_layer, game_state.nav_nodes)

                elif event.button == 1:
                    selected_node = None
                    for each_id, each_node in game_state.nav_nodes.items():
                        if utilities.check_if_inside(each_node.x - 3,
                                                     each_node.x + 3,
                                                     each_node.y - 3,
                                                     each_node.y + 3,
                                                     (mouse_x, mouse_y)):
                            selected_node = each_node
                            break
                    if selected_node:
                        node_to_delete = add_neighbors(screen, scroll_x, scroll_y, game_state, selected_node)
                        selected_node = None
                        if node_to_delete:
                            del game_state.nav_nodes[node_to_delete]
                            bad_edges = []
                            for each_id, each_edge in game_state.nav_edges.items():
                                point_a, point_b = each_edge.points

                                if id(point_a) == node_to_delete or id(point_b) == node_to_delete:
                                    bad_edges.append(each_id)
                            for each in bad_edges:
                                del game_state.nav_edges[each]
                            update_node_layer(game_state.node_layer, game_state.nav_nodes)
                            update_nav_edge_layer(game_state.nav_edge_layer, game_state.nav_edges)
            elif event.type == pygame.KEYDOWN:
                scroll_x, scroll_y = scroll_handler(event, scroll_x, scroll_y)
                if event.key == pygame.K_d:
                    placing_nodes = False
                    print("done placing nodes")
        draw_to_screen(screen, scroll_x, scroll_y, game_state, True)
        pygame.display.flip()


def new_game():
    new_game = GameState()
    new_game.player = Player()
    port_layer_width = assets.map_image.get_width()
    port_layer_height = assets.map_image.get_height()
    node_layer_width = assets.map_image.get_width()
    node_layer_height = assets.map_image.get_height()
    new_game.port_layer = pygame.Surface([port_layer_width, port_layer_height])
    new_game.node_layer = pygame.Surface([node_layer_width, node_layer_height])
    new_game.nav_edge_layer = pygame.Surface([node_layer_width, node_layer_height])
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
    new_game.randomize_port_demand()
    update_port_layer(new_game.port_layer, new_game.ports)
    update_node_layer(new_game.node_layer, new_game.nav_nodes)
    update_nav_edge_layer(new_game.nav_edge_layer, new_game.nav_edges)
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
                elif event.key == pygame.K_n:
                    place_nodes(screen, scroll_x, scroll_y, game_state)
                scroll_x, scroll_y = scroll_handler(event, scroll_x, scroll_y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for key, value in game_state.ports.items():
                    if utilities.check_if_inside(value.x + scroll_x,
                                                 value.x + scroll_x + 10,
                                                 value.y + scroll_y,
                                                 value.y + scroll_y + 10,
                                                 pos):
                        port_popup = ui.PortPopup(screen,
                                                  game_state.player,
                                                  value)
                        goto = port_popup.menu_onscreen()
                        if goto:
                            game_state.player.ship.x = value.x
                            game_state.player.ship.y = value.y
                            draw_to_screen(screen, scroll_x, scroll_y, game_state)
                        if game_state.player.ship.x == value.x and game_state.player.ship.y == value.y:
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
