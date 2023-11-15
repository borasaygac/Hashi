import sympy
from sympy import *


# This file is for parsing the input files


def get_game_field_size():
    # Gets game field from input .txt file and sets the size of the game.

    # Opens the file, reads everything. Prints a list. Since the first two numbers always indicate
    # x and y size, sets these manually. Creates a list with all the islands, their locations and
    # the number of bridges.
    file = 'Project_1/test22.txt'
    with open(file) as t:  # to do: parse until space and do it again
        size_info = t.readline()
        size_info = size_info.split()
        x_size = int(size_info[0])
        y_size = int(size_info[1])

    with open(file) as t:  # to do: parse until space and do it again
        contents = t.readlines()

    return x_size, y_size, contents


def get_island_location(x_size, y_size, contents):
    island_location = list()

    for i in range(1, x_size + 1):
        for j in range(y_size):
            if contents[i][j] != '.':
                island_location.append((i - 1, j, int(contents[i][j])))

    return island_location


# Initializes the field.
def field_initialization(x_size, y_size, island_location):
    field = [["." for x in range(y_size)] for y in range(x_size)]  # Creates a 2D-Array all set with dots.

    counter = 0
    for _ in range(0, len(island_location)):  # Puts the islands on the field.
        field[island_location[counter][0]][island_location[counter][1]] = island_location[counter][2]
        counter += 1

    for j in range(0, len(field)):
        for i in range(0, len(field)):
            print(field[i])

        return field


def constraints(field, island_location):
    class Node:
        def __init__(self, x, y, bridge_no, horizontal_bridge1=False, horizontal_bridge2=False, vertical_bridge1=False,
                     vertical_bridge2=False):
            self.x = x
            self.y = y
            self.bridge_no = bridge_no
            self.horizontal_bridge1 = horizontal_bridge1
            self.horizontal_bridge2 = horizontal_bridge2
            self.vertical_bridge1 = vertical_bridge1
            self.vertical_bridge2 = vertical_bridge2

    nodes = [[Node(0, 0, 0) for x in range(len(field))] for y in range(len(field))]

    for i in range(0, len(field)):
        for j in range(0, len(field)):
            if field[i][j] != '.':
                island = Node(i, j, field[i][j], True, True, True, True)
                nodes[i][j] = island
            else:
                non_island = Node(i, j, 0)
                nodes[i][j] = non_island

    cross_constraint = true
    con_constraint = true
    start_and_end_constraint = true
    
    for i in range(0, len(field)):
        for j in range(0, len(field)):
            h1, v1, h2, v2 = symbols(f'h_{i}_{j},v_{i}_{j},dh_{i}_{j},dv_{i}_{j}')
            if nodes[i][j].bridge_no == 0:
                cross_constraint = And(cross_constraint, (~ h1 | ~ v1), (~ h2 | ~ v2))
                h3, v3, h4, v4 = symbols(f'h_{i}_{j - 1},v_{i - 1}_{j},h_{i}_{j + 1},v_{i + 1}_{j}')
                
                if i >= 1:
                    con_constraint = And(con_constraint, (~ v1 | v3))
                if i < len(field) - 1:
                    con_constraint = And(con_constraint, (~ v1 | v4))
                if j >= 1:
                    con_constraint = And(con_constraint, (~ h1 | h3))
                if j < len(field) - 1:
                    con_constraint = And(con_constraint, (~ h1 | h4))
            else:
                h1 = sympy.true
                v1 = sympy.true
                h2 = sympy.true
                v2 = sympy.true
                start_and_end_constraint = And(start_and_end_constraint, h1, v1, h2, v2)
                
    formula = And(cross_constraint, con_constraint, start_and_end_constraint)

    print(formula)


def main():
    field_info = get_game_field_size()
    island_info = get_island_location(field_info[0], field_info[1], field_info[2])
    field = field_initialization(x_size=field_info[0], y_size=field_info[1], island_location=island_info)
    constraints(field, island_info)


if __name__ == "__main__":
    main()
