from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

def solve_function(vpool, f):
    # This function takes the formula f as input and tries to solve
    with Solver(bootstrap_with=f) as s:
        s.solve()
        print("\nModel:")
        model = s.get_model()

    res = list(map(lambda x: vpool.obj(x) if x > 0 else '~' + vpool.obj(-x), model))
    print(res)

    return model