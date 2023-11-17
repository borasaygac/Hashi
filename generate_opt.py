from itertools import combinations

arr = [0, 1, 2, 3, 4, 5, 6, 7]
bridge_sum = {}

for r in range(1, 5):  # We're interested in lengths 1 to 4
    for perm in combinations(arr, r):
        count_hor = 0  # Counter for even numbers
        count_ver = 0
        total = 0
        for num in perm:
            if num <= 3:
                count_ver += 1
            else:
                count_hor += 1
        if count_hor > 2 | count_ver > 2:
            continue
        
        total = sum(2 if x % 2 == 0 else 1 for x in perm)

        if total not in bridge_sum:
             bridge_sum[total] = []
        bridge_sum[total].append(perm)

for i in range(1,9):
    print(f"bridge_sum[{i}] = {bridge_sum[i]}")