import nom
import utilities
import queue


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

    def __lt__(self, other):
        return False

    def remove_neighbor_id(self, old_id):
        remaining_neighbors = []
        for each_id in self.neighbors:
            if each_id != old_id:
                remaining_neighbors.append(each_id)
        self.neighbors = remaining_neighbors


class MapEdge(object):
    def __init__(self, x, y, a, b):
        self.id_tag = None
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.points = []
        self.cost = 1

    def __lt__(self, other):
        return False


class Path(object):
    def __init__(self):
        self.nodes = []
        self.steps = []
        self.edges = []


def find_edge(nav_mesh, point_a, point_b):
    for edge_id, edge in nav_mesh.edges.items():
        if edge.points[0] is point_a and edge.points[1] is point_b:
            return edge_id
        elif edge.points[0] is point_b and edge.points[1] is point_a:
            return edge_id
    return None


def explore_frontier_to_target(nav_mesh, visited, target_node, closest_node, frontier):
    while not frontier.empty():
        priority, current_node, previous_node = frontier.get()
        edge_id = find_edge(nav_mesh, previous_node, current_node)
        assert edge_id is not None
        edge = nav_mesh.edges[edge_id]
        new_steps = visited[previous_node][0] + edge.cost
        if current_node not in visited or new_steps < visited[current_node][0]:
            node_neighbors = current_node.neighbors
            for each_node in node_neighbors:
                if nav_mesh.nodes[each_node] == target_node or nav_mesh.nodes[each_node].passable:
                    priority = new_steps
                    frontier.put((priority, nav_mesh.nodes[each_node], current_node))
            visited[current_node] = (new_steps, previous_node)
        if target_node in visited:
            break
    assert target_node in visited
    return visited, target_node


def get_path(start_node_id, nav_mesh, target_node_id):
    target_node = nav_mesh.nodes[target_node_id]
    start_node = nav_mesh.nodes[start_node_id]
    visited = {start_node: (0, None)}
    frontier = queue.PriorityQueue()
    closest_node = start_node
    for each in start_node.neighbors:
        if nav_mesh.nodes[each].passable:
            edge_id = find_edge(nav_mesh, start_node, nav_mesh.nodes[each])
            frontier.put((nav_mesh.edges[edge_id].cost, nav_mesh.nodes[each], start_node))
    visited, closest_node = explore_frontier_to_target(nav_mesh, visited, target_node, closest_node, frontier)
    assert closest_node in visited

    new_path = Path()
    new_path.nodes.append(closest_node)
    new_path.steps.append(closest_node)
    new_path.steps.append(visited[closest_node][1])
    while start_node not in new_path.nodes:
        next_node = new_path.steps[-1]
        if next_node != start_node:
            new_path.steps.append(visited[next_node][1])
        new_path.nodes.append(next_node)
    new_path.nodes.reverse()
    # removes the start tile from the tiles list and the steps list in the path object
    new_path.nodes.pop(0)
    new_path.steps.reverse()
    new_path.steps.pop(0)
    edge_id = find_edge(nav_mesh, start_node, new_path.steps[0])
    first_edge = nav_mesh.edges[edge_id]
    new_path.edges.append(first_edge)
    for each in new_path.steps:
        if each is not new_path.steps[-1]:
            this_point_index = new_path.steps.index(each)
            next_point = new_path.steps[this_point_index + 1]
            edge_id = find_edge(nav_mesh, each, next_point)
            edge = nav_mesh.edges[edge_id]
            new_path.edges.append(edge)
    assert len(new_path.edges) == len(new_path.steps)
    return new_path

