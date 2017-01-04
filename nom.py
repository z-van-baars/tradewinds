import random
import os

letters = ["A", "B", "C", "D",
           "E", "F", "G", "H",
           "I", "J", "K", "L",
           "M", "N", "O", "P",
           "Q", "R", "S", "T",
           "U", "V", "W", "X",
           "Y", "Z"]
numbers = ['0', '1', '2', '3',
           '4', '5', '6', '7',
           '8', '9']


def get_id_tag():
    id_string = "{0}{1}{2}{3}{4}".format(random.choice(letters),
                                         random.choice(letters),
                                         random.choice(letters),
                                         random.choice(numbers),
                                         random.choice(numbers))
    return id_string


def read_saved_nodes(map_file):
    text_lines = map_file.readlines()
    reading_nodes = False
    nodes = {}
    print('Retrieving nodes...')
    for line in text_lines:
        if reading_nodes is True and line != "END NODE LIST\n":
            if line[0] == "$":
                print("reading a node...")
                id_string = line[1:-1]
                x = int(text_lines[text_lines.index(line) + 1][:-1])
                y = int(text_lines[text_lines.index(line) + 2][:-1])
                neighbors = text_lines[text_lines.index(line) + 3][:-1]
                neighbors = neighbors.split()
                for each in neighbors:
                    assert each != " "
                nodes[id_string] = [x, y, neighbors]
        elif reading_nodes is True and line == "END NODE LIST\n":
            reading_nodes = False
        if line == "START NODE LIST\n":
            reading_nodes = True
    return nodes


def read_saved_edges(map_file):
    text_lines = map_file.readlines()


def save_nav_mesh(nodes):
    print("Saving nav mesh...")
    map_file = open("maps/MAP_001.txt", 'w')
    map_file.write('START NODE LIST\n')
    map_file.write('\n')
    for each_id, each_node in nodes.items():
        map_file.write('${0}\n'.format(each_id))
        map_file.write(str(each_node.x) + '\n')
        map_file.write(str(each_node.y) + '\n')
        neighbor_string = ''
        for each in each_node.neighbors:
            neighbor_string = neighbor_string + each + ' '
        neighbor_string = neighbor_string + '\n'
        map_file.write(neighbor_string)
        map_file.write('\n')
    map_file.write('\n')
    map_file.write("END NODE LIST\n")
    map_file.write('\n')
    print("...Done")