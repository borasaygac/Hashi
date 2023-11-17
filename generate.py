from itertools import permutations

arr = [0, 1, 2, 3, 4, 5, 6, 7]
bridge_sum = {}

for r in range(1, 5):  # We're interested in lengths 1 to 4
     for perm in permutations(arr, r):
         count = sum(2 if num % 2 == 0 else 1 for num in perm)
         if count not in bridge_sum:
             bridge_sum[count] = []
         bridge_sum[count].append(perm)
