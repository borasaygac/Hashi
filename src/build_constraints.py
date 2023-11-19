import sympy
from pysat.formula import CNF, IDPool
from assets.bridge_sum import bridge_sum_CNF as bridge_sum
import math


def build_constraints(field):
    # Create a class named Node representing holding boolean variables.
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

    f = CNF()
    n = [[Node(0) for _ in range(len(field[0]))] for _ in range(len(field))]
    # variable pool for formula
    vpool = IDPool()
    v = lambda i: vpool.id('{0}'.format(i)) 

    def initialize_nodes():
        for i in range(0, len(field)):
            for j in range(0, len(field[0])):
                    n[i][j] = Node(field[i][j] if field[i][j]!='.' else 0, v(f'h_{i}_{j}'), v(f'dh_{i}_{j}'), v(f'v_{i}_{j}'), v(f'dv_{i}_{j}'))
        return n

    n = initialize_nodes()  
    def build_constraints():
        for i in range(0, len(field)):
            for j in range(0, len(field[0])):
                if n[i][j].val == 0:
                    # no cross: only one type of bridge on none island nodes
                    f.extend([[-n[i][j].h1, -n[i][j].v1], [-n[i][j].h2, -n[i][j].v2],
                              [-n[i][j].h1, -n[i][j].v2], [-n[i][j].h2, -n[i][j].v1],
                              [-n[i][j].h1, -n[i][j].h2], [-n[i][j].v1, -n[i][j].v2]
                             ])
                    # continuity: bridges extend from an island node to an island node  
                    if i >= 1:
                        f.extend([[-n[i][j].v1, n[i - 1][j].v1], [-n[i][j].v2, n[i - 1][j].v2]])
                    if i < len(field) - 1:
                        f.extend([[-n[i][j].v1, n[i + 1][j].v1], [-n[i][j].v2, n[i + 1][j].v2]])
                    if j >= 1:
                        f.extend([[-n[i][j].h1, n[i][j - 1].h1], [-n[i][j].h2, n[i][j - 1].h2]])
                    if j < len(field) - 1:
                        f.extend([[-n[i][j].h1, n[i][j + 1].h1], [-n[i][j].h2, n[i][j + 1].h2]])
                else:
                    # start_and_end: bridges need to start from and end at islands
                    f.extend([[n[i][j].h1], [n[i][j].v1], [n[i][j].h2], [n[i][j].v2]])
                    
                    # degree: bridges built by an island must be equal to its node val
                    clauses = bridge_sum[n[i][j].val]
                    
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
                    if j < len(field) - 1:
                        mapping[7] = n[i][j+1].h1
                        mapping[8] = n[i][j+1].h2
                    
                    filtered_clauses = []
                    for row in clauses:
                        filtered = list(filter(lambda x: x < 0, row))
                        if (len(filtered) > 0 and all(abs(el) in mapping for el in filtered)) or len(filtered) ==0:
                            filtered_clauses.append(row)
                                   
                    mapped_clauses = [[int(math.copysign(1, literal))*mapping[abs(literal)] for literal in clause] for clause in filtered_clauses]
                    res = [[vpool.obj(literal) if literal > 0 else '~' + vpool.obj(-literal) for literal in clause] for clause in mapped_clauses]
                    f.extend(mapped_clauses)

    build_constraints()
    return n, vpool, f

    # with Solver(bootstrap_with=f) as s:
    #         s.solve()
    #         print("\nModel:")
    #         for m in s.enum_models():
    #             print(m)
