from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


def solve(vpool, f):
    with Solver(bootstrap_with=f) as s:
        s.solve()
        print("\nModel:\n")
        model = s.get_model()

    if model is None:
        return
    print(list(map(lambda x: vpool.obj(x) if x > 0 else '~' + vpool.obj(-x), model)))
    return model
