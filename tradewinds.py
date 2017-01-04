import pygame
import calendar
import port
import assets
import ui
import utilities
import ships
import display
import navigate
import nom
import os

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
        self.nav_mesh = None

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
                        game_state.update_port_layer(game_state.port_layer, game_state.ports)
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
    screen.blit(game_state.display.port_layer, [scroll_x, scroll_y])
    screen.blit(game_state.display.node_layer, [scroll_x, scroll_y])
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
        screen.blit(game_state.display.edge_layer, [scroll_x, scroll_y])
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


def add_neighbors_right_click(selected_node, mouse_x, mouse_y, nav_mesh, nodes, edges):
    hitbox_tolerance = 6
    """Pixel tolerance on screen to accomodate for fat fingering.  Smaller is more precise but harder
    to hit, wider is easier to hit but less accurate."""

    new_neighbor_id = None
    for each_id, each_node in nodes.items():
        if utilities.check_if_inside(each_node.x - hitbox_tolerance,
                                     each_node.x + hitbox_tolerance,
                                     each_node.y - hitbox_tolerance,
                                     each_node.y + hitbox_tolerance,
                                     (mouse_x, mouse_y)):
            new_neighbor_id = each_id
            break
    if new_neighbor_id:
        print("Trying to add neighbor {0}...".format(new_neighbor_id))
        if new_neighbor_id not in selected_node.neighbors:
            selected_node.neighbors.append(new_neighbor_id)

            duplicate_edge = False
            for each_id, each_edge in edges.items():
                point_a = each_edge.points[0]
                point_b = each_edge.points[1]
                duplicate_edge = nav_mesh.edge_match_check(each_edge,
                                                           point_a,
                                                           point_b,
                                                           selected_node.id_tag,
                                                           new_neighbor_id)
            if not duplicate_edge:
                print("Added a new Edge!")
                new_neighbor_node = nodes[new_neighbor_id]
                new_neighbor_node.neighbors.append(selected_node.id_tag)
                neighbor_x, neighbor_y = new_neighbor_node.x, new_neighbor_node.y
                nav_mesh.add_edge(selected_node.x,
                                  selected_node.y,
                                  neighbor_x,
                                  neighbor_y,
                                  selected_node,
                                  new_neighbor_node)
            else:
                print("This edge already exists!")
    else:
        print("Try clicking on a node next time.")


def add_neighbors(screen, scroll_x, scroll_y, game_state, selected_node):
    print("adding neighbors to {0}".format(selected_node.id_tag))
    print("Coordinates are: {0}  {1}".format(selected_node.x, selected_node.y))
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
                    add_neighbors_right_click(selected_node,
                                              mouse_x,
                                              mouse_y,
                                              game_state.nav_mesh,
                                              game_state.nav_mesh.nodes,
                                              game_state.nav_mesh.edges)
                    game_state.display.update(game_state.ports, game_state.nav_mesh.nodes, game_state.nav_mesh.edges)

                elif event.button == 1:
                    selected_node = None
                    adding_neighbors = False

            elif event.type == pygame.KEYDOWN:
                scroll_x, scroll_y = scroll_handler(event, scroll_x, scroll_y)
                if event.key == pygame.K_d:
                    node_to_delete_id = selected_node.id_tag
                    adding_neighbors = False
                    return node_to_delete_id
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
                    game_state.nav_mesh.add_node(mouse_x, mouse_y, True)
                    game_state.display.update(game_state.ports, game_state.nav_mesh.nodes, game_state.nav_mesh.edges)

                elif event.button == 1:
                    selected_node = None
                    for each_id, each_node in game_state.nav_mesh.nodes.items():
                        if utilities.check_if_inside(each_node.x - 3,
                                                     each_node.x + 3,
                                                     each_node.y - 3,
                                                     each_node.y + 3,
                                                     (mouse_x, mouse_y)):
                            selected_node = each_node
                            break
                    if selected_node:
                        node_to_delete_id = add_neighbors(screen, scroll_x, scroll_y, game_state, selected_node)
                        if node_to_delete_id:
                            print("deleting a Node")
                            for each_neighbor_id in selected_node.neighbors:
                                game_state.nav_mesh.nodes[each_neighbor_id].remove_neighbor_id(node_to_delete_id)
                            del game_state.nav_mesh.nodes[node_to_delete_id]
                            bad_edges = []
                            for each_id, each_edge in game_state.nav_mesh.edges.items():
                                point_a, point_b = each_edge.points
                                if point_a.id_tag == node_to_delete_id or point_b.id_tag == node_to_delete_id:
                                    bad_edges.append(each_id)
                            for each in bad_edges:
                                del game_state.nav_mesh.edges[each]
                            game_state.display.update(game_state.ports, game_state.nav_mesh.nodes, game_state.nav_mesh.edges)
                        selected_node = None
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
    map_pixel_width = assets.map_image.get_width()
    map_pixel_height = assets.map_image.get_height()
    new_game.display = display.MapDisplayLayer(map_pixel_width, map_pixel_height)
    new_game.nav_mesh = navigate.MapMesh(map_pixel_width, map_pixel_height)

    if os.path.exists("maps/MAP_001.txt"):
        map_node_file = open("maps/MAP_001.txt", 'r+')
        nodes = nom.read_saved_nodes(map_node_file)
        new_game.nav_mesh.rebuild_nav_mesh(nodes)

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
    new_game.display.update(new_game.ports, new_game.nav_mesh.nodes, new_game.nav_mesh.edges)
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
                elif event.key == pygame.K_s:
                    nom.save_nav_mesh(game_state.nav_mesh.nodes)
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
