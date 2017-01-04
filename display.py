import pygame
import assets


class MapDisplayLayer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.node_layer = pygame.Surface([width, height])
        self.edge_layer = pygame.Surface([width, height])
        self.port_layer = pygame.Surface([width, height])

    def update(self, ports, nodes, edges):
        self.update_node_layer(nodes)
        self.update_port_layer(ports)
        self.update_edge_layer(edges)

    def update_edge_layer(self, list_of_edges):
        edge_layer = self.edge_layer
        print(len(list_of_edges))
        edge_layer.fill(assets.key_color)
        small_font = pygame.font.SysFont("Calibri", 10, True, False)
        for each_id, each_edge in list_of_edges.items():
            pygame.draw.line(edge_layer,
                             (255, 40, 40),
                             (each_edge.points[0].x, each_edge.points[0].y),
                             (each_edge.points[1].x, each_edge.points[1].y))
        edge_layer.set_colorkey(assets.key_color)

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
            edge_layer.blit(backing, [cost_x, cost_y])

    def update_port_layer(self, list_of_ports):
        port_layer = self.port_layer
        port_layer.fill(assets.key_color)
        for each in list_of_ports:
            port_layer.blit(assets.port_marker, [list_of_ports[each].x, list_of_ports[each].y])
        port_layer.set_colorkey(assets.key_color)
        port_layer = port_layer.convert_alpha()
        print("Updated port layer")

    def update_node_layer(self, list_of_nodes):
        node_layer = self.node_layer
        node_layer.fill(assets.key_color)
        for each in list_of_nodes:
            node_layer.blit(assets.node_marker, [list_of_nodes[each].x - 3, list_of_nodes[each].y - 3])
        node_layer.set_colorkey(assets.key_color)
        node_layer = node_layer.convert_alpha()
    print("Updated node layer")
