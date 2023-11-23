from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


def solve(vpool, f, neighbours, y):

    # interconnectivity: perform dfs on models to extract connected solution

    def dfs(island, model, neighbours, counter, seen):
        def pos(i, j): return 4*(y*i+j)
        i, j = island[0], island[1]

        right = model[pos(i, j+1):(pos(i, j+1)+4)]
        down = model[pos(i+1, j):(pos(i+1, j)+4)]
        left = model[(pos(i, j-1)):(pos(i, j-1)+4)]
        up = model[(pos(i-1, j)):(pos(i-1, j)+4)]

        if (right[0] > 0 or right[1] > 0) and (neighbours[(i, j)][0] not in seen):
            seen.add(neighbours[(i, j)][0])
            counter += dfs(neighbours[(i, j)][0], model, neighbours, 1, seen)

        if (down[2] > 0 or down[3] > 0) and (neighbours[(i, j)][1] not in seen):
            seen.add(neighbours[(i, j)][1])
            counter += dfs(neighbours[(i, j)][1], model, neighbours, 1, seen)

        if (left[0] > 0 or left[1] > 0) and (neighbours[(i, j)][2] not in seen):
            seen.add(neighbours[(i, j)][2])
            counter += dfs(neighbours[(i, j)][2], model, neighbours, 1, seen)

        if (up[2] > 0 or up[3] > 0) and (neighbours[(i, j)][3] not in seen):
            seen.add(neighbours[(i, j)][3])
            counter += dfs(neighbours[(i, j)][3], model, neighbours, 1, seen)

        return counter

    with Solver(bootstrap_with=f) as s:
        s.solve()
        print("\nModel:\n")
        for m in s.enum_models():
            start = list(neighbours.keys())[0]
            seen = set(start)

            if dfs(start, m, neighbours, 0, seen) == len(neighbours.keys()):
                print(list(map(lambda x: vpool.obj(x) if x >
                      0 else '~' + vpool.obj(-x), m)))
                print()
                return m
    return None
