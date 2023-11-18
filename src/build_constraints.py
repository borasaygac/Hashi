import sympy
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

from solve import solve


def build_constraints(field):
    # Create a class named Node representing each x and y value on the field.
    class Node:
        def __init__(self,
                     bridge_no,  # Number of bridges on a given node [ bridge_no element of (0,8)].
                     # hb(X) and vb(Y) refer to the horizontal and vertical bridges. Set to true by default.
                     # The rules of Hashi explain that an island can have at most 2 bridges running in each direction.
                     horizontal_bridge1=sympy.true,
                     horizontal_bridge2=sympy.true,
                     vertical_bridge1=sympy.true,
                     vertical_bridge2=sympy.true):
            self.val = bridge_no
            self.h1 = horizontal_bridge1
            self.h2 = horizontal_bridge2
            self.v1 = vertical_bridge1
            self.v2 = vertical_bridge2

    f = CNF()
    n = [[Node(0) for x in range(len(field[0]))] for y in range(len(field))]
    # Initializes n*m Nodes, by len(field[0]) = n and len(field) = m.
    # Nodes have 0 bridges through this initialization.
    vpool = IDPool()

    def vpool_format():  # For debugging purposes the Lambda function has been nestled into a function.
        return lambda i: vpool.id('{0}'.format(i))

    v = vpool_format()  # Assigns the formatted vpool to v.

    def initialize_nodes_and_extend_formula():
        for i in range(0, len(field)):  # Initializes the Nodes along x and then y.
            for j in range(0, len(field[0])):
                if field[i][j] == '.':
                    # If this x,y on the field is NOT an island, then create a Node object with
                    # Bridge_no = 0, h1 = h_x_y, h2 = dh_x_y, v1 = v_x_y, v2 = dv_x_y
                    # dh and dv implies double horizontal or double vertical.
                    n[i][j] = Node(0, v(f'h_{i}_{j}'), v(f'dh_{i}_{j}'), v(f'v_{i}_{j}'), v(f'dv_{i}_{j}'))
                else:
                    # If this x,y on the field IS an island, then create a Node Object with bridge_no equal to
                    # that in the parsed field.
                    # Then extend the CNF formula f with h1,h2,v1,v2 per Node.
                    n[i][j] = Node(field[i][j], v(f'h_{i}_{j}'), v(f'dh_{i}_{j}'), v(f'v_{i}_{j}'), v(f'dv_{i}_{j}'))
                    f.extend([[n[i][j].h1], [n[i][j].v1], [n[i][j].h2], [n[i][j].v2]])
        return n

    n = initialize_nodes_and_extend_formula()

    # TODO: Check later whether we need this or not
    # a = [[Node(0, Atom(n[x][y].h1), Atom(n[x][y].h2), Atom(n[x][y].v1), Atom(n[x][y].v2)) for y in range(len(field[0]))]
    #      for x in range(len(field))]

    def bridge_only_in_one_direction():
        for i in range(0, len(field)):
            for j in range(0, len(field[0])):
                if n[i][j].val == 0:
                    # For all Nodes in a field of size i * j:
                    # IF the node is NOT an island -> then extend f with the following formula:
                    # (NOT h1_x_y OR NOT v1_x_y) AND (NOT h2_x_y OR NOT v2_x_y) AND
                    # (NOT h1_x_Y OR NOT v2_x_y) AND (NOT h2_x_y OR NOT v1_x_y)
                    # This means that we're checking for vertical and horizontal bridges occurring at the same time
                    # and ensuring they don't. Permutations are considered.
                    f.extend([[-n[i][j].h1, -n[i][j].v1], [-n[i][j].h2, -n[i][j].v2],
                              [-n[i][j].h1, -n[i][j].v2], [-n[i][j].h2, -n[i][j].v1]]
                             )
                    # These are checks based on location that ensure the bridges
                    # carry on only in one direction.
                    if i >= 1:
                        f.extend([[-n[i][j].v1, n[i - 1][j].v1], [-n[i][j].v2, n[i - 1][j].v2]])
                    if i < len(field) - 1:
                        f.extend([[-n[i][j].v1, n[i + 1][j].v1], [-n[i][j].v2, n[i + 1][j].v2]])
                    if j >= 1:
                        f.extend([[-n[i][j].h1, n[i][j - 1].h1], [-n[i][j].h2, n[i][j - 1].h2]])
                    if j < len(field) - 1:
                        f.extend([[-n[i][j].h1, n[i][j + 1].h1], [-n[i][j].h2, n[i][j + 1].h2]])

    bridge_only_in_one_direction()

    return n, vpool, f # TODO: this seems too specific, should we delete it?

    # with Solver(bootstrap_with=f) as s:
    #         s.solve()
    #         print("\nModel:")
    #         for m in s.enum_models():
    #             print(m)
