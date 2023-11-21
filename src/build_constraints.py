from pysat.formula import CNF, IDPool
from assets.bridge_sum import bridge_sum_CNF as bridges
import math


def build_constraints(field, neighbours):
    class Node:
        def __init__(self,
                     bridge_no,
                     horizontal_bridge1=None,
                     horizontal_bridge2=None,
                     vertical_bridge1=None,
                     vertical_bridge2=None):
            self.val = bridge_no
            self.h1 = horizontal_bridge1
            self.h2 = horizontal_bridge2
            self.v1 = vertical_bridge1
            self.v2 = vertical_bridge2

    # formula f, nodes array n, variable pool vpool
    f = CNF()
    n = [[Node(0) for _ in range(len(field[0]))] for _ in range(len(field))]
    vpool = IDPool()
    v = lambda i: vpool.id('{0}'.format(i)) 

    def initialize_nodes():
        for i in range(0, len(field)):
            for j in range(0, len(field[0])):
                    n[i][j] = Node(field[i][j], v(f'h_{i}_{j}'), v(f'dh_{i}_{j}'), v(f'v_{i}_{j}'), v(f'dv_{i}_{j}'))
        return n

    n = initialize_nodes()
        
    def build_constraints():
        for i in range(1, len(field)-1):
            for j in range(1, len(field[0])-1):
                if n[i][j].val == 0:
                    # no cross: only one type of bridge on none island nodes
                    f.extend([[-n[i][j].h1, -n[i][j].v1], [-n[i][j].h2, -n[i][j].v2],
                              [-n[i][j].h1, -n[i][j].v2], [-n[i][j].h2, -n[i][j].v1],
                              [-n[i][j].h1, -n[i][j].h2], [-n[i][j].h2, -n[i][j].h1],
                              
                              [-n[i][j].v1, -n[i][j].h1], [-n[i][j].v2, -n[i][j].h1],
                              [-n[i][j].v1, -n[i][j].v2], [-n[i][j].v2, -n[i][j].v1],
                              [-n[i][j].v1, -n[i][j].h2], [-n[i][j].v2, -n[i][j].h2],
                              
                             ])
                    
                    #continuity: bridges extend from an island node to an island node  
                    if i >= 1:
                        f.extend([[-n[i][j].v1, n[i - 1][j].v1], [-n[i][j].v2, n[i - 1][j].v2]])
                    if i < len(field) - 1:
                        f.extend([[-n[i][j].v1, n[i + 1][j].v1], [-n[i][j].v2, n[i + 1][j].v2]])
                    if j >= 1:
                        f.extend([[-n[i][j].h1, n[i][j - 1].h1], [-n[i][j].h2, n[i][j - 1].h2]])
                    if j < len(field[0]) - 1:
                        f.extend([[-n[i][j].h1, n[i][j + 1].h1], [-n[i][j].h2, n[i][j + 1].h2]])
                else:
                    
                    # neighbours: if there are no neighbouring island
                    # in any direction, we do not build in that direction 
                    neighbour_cells = neighbours[(i, j)]
                    if neighbour_cells[0] is None:
                        f.extend([[-n[i][j + 1].h1], [-n[i][j + 1].h2]])
                    if neighbour_cells[1] is None:
                        f.extend([[-n[i + 1][j].v1], [-n[i + 1][j].v2]])
                    if neighbour_cells[2] is None:
                        f.extend([[-n[i][j - 1].h1], [-n[i][j - 1].h2]])
                    if neighbour_cells[3] is None:
                        f.extend([[-n[i - 1][j].v1], [-n[i - 1][j].v2]])

                    # start_and_end: bridges need to start from and end at islands
                    f.extend([[n[i][j].h1], [n[i][j].v1], [n[i][j].h2], [n[i][j].v2]])
                    
                    # degree: bridges built by an island must be equal to its node val
                    clauses = bridges[n[i][j].val]
                    
                    # Since the clauses carry index integers, we need to map them to their corresponding value
                    mapping = {}
                    
                    if i >= 1:
                        mapping[1] = n[i-1][j].v1
                        mapping[2] = n[i-1][j].v2                        
                    if i < len(field) - 1:
                        mapping[3] = n[i+1][j].v1
                        mapping[4] = n[i+1][j].v2     
                    if j >= 1:
                        mapping[5] = n[i][j-1].h1
                        mapping[6] = n[i][j-1].h2  
                    if j < len(field[0]) - 1:
                        mapping[7] = n[i][j+1].h1
                        mapping[8] = n[i][j+1].h2
                                        
                    mapped_clauses = [[int(math.copysign(1, literal))*mapping[abs(literal)] for literal in clause] for clause in clauses]
                    
                    f.extend(mapped_clauses)
                    
    build_constraints()
    return n, vpool, f
