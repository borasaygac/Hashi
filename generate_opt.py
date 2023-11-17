from itertools import combinations

arr = [0, 1, 2, 3, 4, 5, 6, 7]
bridge_sum = {}

for r in range(1, 5):  # We're interested in lengths 1 to 4
    for comb in combinations(arr, r):
        s = set()
        subsequent_pair = False
        count_hor = 0  # Counter for even numbers
        count_ver = 0
        total = 0
        for num in comb:
            if num <= 3:
                count_ver += 1
            else:
                count_hor += 1
            if(((num-1) in s) & (num != 4) & (num % 2 == 1)):
                subsequent_pair = True
            else:
                s.add(num)
        if (count_hor > 2) | (count_ver > 2) | (subsequent_pair): # prevent subsequent pairs and more than 3 bridges built along the same axis 
            continue
        
        total = sum(2 if x % 2 == 0 else 1 for x in comb)
        if total not in bridge_sum:
             bridge_sum[total] = []
        bridge_sum[total].append(set(comb))

for i in range(1,9):
    print(f"bridge_sum[{i}] = {bridge_sum[i]}")