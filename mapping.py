##FOR MAPPING OF POSSIBLE COMBINATIONS
bridging = [n[i - 1][j].v1, n[i - 1][j].v2, n[i + 1][j].v1, n[i + 1][j].v2,
            n[i][j - 1].h1, n[i][j - 1].h2, n[i][j + 1].h1, n[i][j + 1].h2]

indexes = [1, 2, 3, 4, 5, 6, 7, 8]

all_combinations = list(combinations(indexes, 3))


def calculate_bridge_count(tup):
    return sum(2 if x % 2 == 0 else 1 for x in tup)


bridge_count_map = {tupel: calculate_bridge_count(tup) for tupel in all_combinations}