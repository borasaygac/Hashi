from itertools import combinations

arr = [0, 1, 2, 3, 4, 5, 6, 7]
bridge_sum = {}

for r in range(1, 5):  # We're interested in lengths 1 to 4
    for perm in combinations(arr, r):
        count_even = 0  # Counter for even numbers
        count_odd = 0
        total = 0
        for num in perm:
            if num % 2 == 0:
                count_even += 1
                total += 2 
            else:
                count_odd += 1
                total += 1

        if count_even > 2 | count_odd > 2:
            continue

        if total not in bridge_sum:
             bridge_sum[total] = []
        bridge_sum[total].append(perm)

for i in range(1,9):
    print(f"bridge_sum[{i}] = {bridge_sum[i]}")