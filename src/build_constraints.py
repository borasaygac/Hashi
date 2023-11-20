from pysat.formula import CNF, IDPool
from assets.bridge_sum import bridge_sum_CNF as bridges
import math


def build_constraints(field, neighbours):
    # Create a class named Node representing each x and y value on the field.
    class Node:
        def __init__(self,
                     bridge_no,  # Number of bridges on a given node [ bridge_no element of (0,8)].
                     # hb(X) and vb(Y) refer to the horizontal and vertical bridges. Set to true by default.
                     # The rules of Hashi explain that an island can have at most 2 bridges running in each direction.
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
                    # continuity: bridges extend from an island node to an island node  
                    if i >= 1:
                        f.extend([[-n[i][j].v1, n[i - 1][j].v1], [-n[i][j].v2, n[i - 1][j].v2]])
                    if i < len(field) - 1:
                        f.extend([[-n[i][j].v1, n[i + 1][j].v1], [-n[i][j].v2, n[i + 1][j].v2]])
                    if j >= 1:
                        f.extend([[-n[i][j].h1, n[i][j - 1].h1], [-n[i][j].h2, n[i][j - 1].h2]])
                    if j < len(field[0]) - 1:
                        f.extend([[-n[i][j].h1, n[i][j + 1].h1], [-n[i][j].h2, n[i][j + 1].h2]])
                else:
                    # neighbours: if there are no neighbouring islands 
                    # in one direction, we do not build in that direction 
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
                    
                    # filtered_clauses = clauses
                    # for clause in filtered_clauses:
                    #     for literal in clause:
                    #         if literal < 0 and (abs(literal) not in mapping):
                    #             del clause
                    # condition = lambda row: all(abs(lit) in mapping for lit in row )  # Condition to keep rows with non-negative first element
                    # filtered_clauses = [row for row in clauses if condition(row)]

                                        
                    mapped_clauses = [[int(math.copysign(1, literal))*mapping[abs(literal)] for literal in clause] for clause in clauses]
                    
                    res = [[vpool.obj(literal) if literal > 0 else '~' + vpool.obj(-literal) for literal in clause] for clause in mapped_clauses]
                    f.extend(mapped_clauses)
                         
    # f.extend([[-n[6][0].h1], [-n[6][0].h2], [-n[6][0].v1], [-n[6][0].v2 ]])
    # f.extend([[-n[3][0].h1], [-n[3][0].h2], [-n[3][0].v1], [-n[3][0].v2 ]])
    # f.extend([[-n[0][1].h1], [-n[0][1].h2], [-n[0][1].v1], [-n[0][1].v2 ]])
    # f.extend([[-n[1][0].h1], [-n[1][0].h2], [-n[1][0].v1], [-n[1][0].v2 ]])
    # f.extend([[-n[7][0].h1], [-n[7][0].h2], [-n[7][0].v1], [-n[7][0].v2 ]])
    # f.extend([[-n[0][3].h1], [-n[0][3].h2], [-n[0][3].v1], [-n[0][3].v2 ]])
    # f.extend([[-n[5][8].h1], [-n[5][8].h2], [-n[5][8].v1], [-n[5][8].v2 ]])
    # f.extend([[-n[0][6].h1], [-n[0][6].h2], [-n[0][6].v1], [-n[0][6].v2 ]])
    build_constraints()
    # f.extend([[n[4][1].h1], [n[4][3].h2]])
    return n, vpool, f # TODO: this seems too specific, should we delete it?

    # with Solver(bootstrap_with=f) as s:
    #         s.solve()
    #         print("\nModel:")
    #         for m in s.enum_models():
    #             print(m)
