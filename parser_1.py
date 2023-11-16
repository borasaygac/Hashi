import math
import os
import sympy
import sys
from sympy import *
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver
from itertools import combinations

# This file is for parsing the input files
num = 1

def get_game_field_size(num):
    # Gets game field from input .txt file and sets the size of the game.

    # Opens the file, reads everything. Prints a list. Since the first two numbers always indicate
    # x and y size, sets these manually. Creates a list with all the islands, their locations and
    # the number of bridges.
    file = f'Project_1/test{num}.txt'
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
        def __init__(self, bridge_no, horizontal_bridge1=sympy.true, horizontal_bridge2=sympy.true, vertical_bridge1=sympy.true,
                     vertical_bridge2=sympy.true):
            self.val = bridge_no
            self.h1 = horizontal_bridge1
            self.h2 = horizontal_bridge2
            self.v1 = vertical_bridge1
            self.v2 = vertical_bridge2
    f = CNF()
    n = [[Node( 0) for x in range(len(field))] for y in range(len(field))]
    vpool = IDPool()
    v = lambda i : vpool.id('{0}'.format(i))
    
    for i in range(0, len(field)):
        for j in range(0, len(field)):
            if field[i][j] == '.':
                n[i][j] = Node(0, v(f'h_{i}_{j}'), v(f'dh_{i}_{j}'), v(f'v_{i}_{j}'), v(f'dv_{i}_{j}'))
            else:
                n[i][j] = Node(field[i][j], v(f'h_{i}_{j}'), v(f'dh_{i}_{j}'), v(f'v_{i}_{j}'), v(f'dv_{i}_{j}'))
                f.extend([[n[i][j].h1],[n[i][j].v1],[n[i][j].h2],[n[i][j].v2] ])
                

    
    for i in range(0, len(field)):
        for j in range(0, len(field)):
            if n[i][j].val == 0:
                f.extend([[-n[i][j].h1, -n[i][j].v1], [-n[i][j].h2, -n[i][j].v2],
                          [-n[i][j].h1, -n[i][j].v2],  [-n[i][j].h2, -n[i][j].v1]]
                         )               
                if (i >= 1):
                   f.extend([[-n[i][j].v1, n[i-1][j].v1], [-n[i][j].v2, n[i-1][j].v2]])
                if (i < len(field) - 1):
                    f.extend([[-n[i][j].v1, n[i+1][j].v1], [-n[i][j].v2, n[i+1][j].v2]])
                if (j >= 1):
                    f.extend([[-n[i][j].h1, n[i][j-1].h1], [-n[i][j].h2, n[i][j-1].h2]])                    
                if (j < len(field) - 1):
                    f.extend([[-n[i][j].h1, n[i][j+1].h1], [-n[i][j].h2, n[i][j+1].h2]]) 
    sol = []
    #f.extend([[n[0][5].v1, n[0][5].h1]])
    with Solver(bootstrap_with=f) as s:
        s.solve()
        print("\nModel:")
        sol = s.get_model()
    
    res = list(map(lambda x: vpool.obj(x) if x > 0 else '~'+ vpool.obj(-x), sol))
    print(res)  
    output_folder = os.path.join(os.getcwd(), 'Solution')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, f'sol{num}.txt')
    with open(output_path, 'w') as file:
        j = 0
        for i in range(0, len(sol), 4):
            if n[(i // 4) // len(n[0])][j].val != 0:
                file.write(f'{n[(i // 4) // len(n[0])][j].val}')
            else:
                chunk = sol[i:i+4]
                    
                if any(elem > 0 for elem in chunk):
                    file.write('b')
                else:
                    file.write('0')
            j += 1    
            if (((i // 4) + 1) % len(n[0])) == 0:
                file.write('\n')
                j = 0 
            else:
                file.write(' ')
def main():
    global num
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
    
    print(f'Running solver on test {num}...\n')        
    field_info = get_game_field_size(num)
    island_info = get_island_location(field_info[0], field_info[1], field_info[2])
    field = field_initialization(x_size=field_info[0], y_size=field_info[1], island_location=island_info)
    constraints(field, island_info)


if __name__ == "__main__":
    main()
