import nom
import utilities


class MapMesh(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nodes = {}
        self.edges = {}

    def add_node(self, x, y, passable, id_tag=None, neighbors=None):
        new_node = MapNode(x, y, passable)
        if id_tag is not None:
            new_node.id_tag = id_tag
        else:
            new_node.id_tag = nom.get_id_tag()
            print("Fetching a random ID")
        assert id_tag not in self.nodes
        if neighbors:
            new_node.neighbors = neighbors
        self.nodes[new_node.id_tag] = new_node

    def get_edge_cost(self, edge):
        raw_cost = utilities.distance(edge.x, edge.y, edge.a, edge.b)
        raw_cost = round(raw_cost / 10) + 1
        return raw_cost

    def add_edge(self, x, y, a, b, point_a, point_b):
        new_edge = MapEdge(x, y, a, b)
        new_edge.id_tag = nom.get_id_tag()
        new_edge.points.append(point_a)
        new_edge.points.append(point_b)
        new_edge.cost = self.get_edge_cost(new_edge)
        self.edges[new_edge.id_tag] = new_edge

    def edge_match_check(self, existing_edge, point_a, point_b, point_y, point_z):
        if point_a.id_tag == point_y and point_b.id_tag == point_z:
            print("this connection already exists!")
            return True
        elif point_a.id_tag == point_z and point_b.id_tag == point_y:
            print("this connection already exists!")
            return True
        return False

    def rebuild_nav_mesh(self, nodes_dict):
        for each_id, attributes_list in nodes_dict.items():
            self.add_node(attributes_list[0], attributes_list[1], True, each_id, attributes_list[2])
        for each_id, each_node in self.nodes.items():
            for neighbor_id in each_node.neighbors:
                duplicate_edge = False
                for each_id, each_edge in self.edges.items():
                    point_a = each_edge.points[0]
                    point_b = each_edge.points[1]
                    duplicate_edge = self.edge_match_check(each_edge, point_a, point_b, each_id, neighbor_id)
                if not duplicate_edge:
                    self.add_edge(each_node.x,
                                  each_node.y,
                                  self.nodes[neighbor_id].x,
                                  self.nodes[neighbor_id].y,
                                  each_node,
                                  self.nodes[neighbor_id])


class MapNode(object):
    def __init__(self, x, y, passable):
        self.id_tag = None
        self.x = x
        self.y = y
        self.neighbors = []
        self.passable = passable
        self.cost = 1


class MapEdge(object):
    def __init__(self, x, y, a, b):
        self.id_tag = None
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.points = []
        self.cost = 1