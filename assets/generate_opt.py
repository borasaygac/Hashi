from itertools import combinations

#[ n[i-1][j].v1,  n[i-1][j].v2, n[i+1][j].v1 , n[i+1][j].v2,  n[i][j-1].h1, n[i][j-1].h2, n[i][j+1].h1, n[i][j+1].h2]

#         |
#    --Island--
#         |
# node.val = 3 => 
arr = [1, 2, 3, 4, 5, 6, 7, 8]
bridge_sum_DNF = {}

for r in range(1, 5):  # We're interested in lengths 1 to 4
    for comb in combinations(arr, r):
        s = set()
        subsequent_pair = False
        count_hor = 0  # Counter for even numbers
        count_ver = 0
        total = 0
        toAdd = set([-1, -2, -3, -4, -5, -6, -7, -8])
        for num in comb:
            if num <= 4:
                count_ver += 1
            else:
                count_hor += 1
            if(((num-1) in toAdd) & (num != 4) & (num % 2 == 1)):
                subsequent_pair = True
            else:
                s.add(num)
            toAdd.add(num)
            toAdd.remove(-num)
            
        if (count_hor > 2) | (count_ver > 2) | (subsequent_pair): # prevent subsequent pairs and more than 3 bridges built along the same axis 
            continue
        
        total = sum(2 if x % 2 == 0 else 1 for x in comb)
        if total not in bridge_sum_DNF:
             bridge_sum_DNF[total] = []
        bridge_sum_DNF[total].append(list(toAdd))
        
for i in range(1,9):
    print(f"bridge_sum_DNF[{i}]=[", end=' ')
    for clause in bridge_sum_DNF[i]:
        print('[', end=' ')
        print(*clause, sep=", ", end=' ')
        print('], ', end=' ')
    print(']')
    
    # Example dictionary of 2D arrays

# Step 1: Merge all lists from the dictionary values into one big list B
bridge_sum_merged = []
for array in bridge_sum_DNF.values():
    for sublist in array:
        bridge_sum_merged.append(sublist)
bridge_sum_CNF = {}

def invert(sublist):
    return [-el for el in sublist]
    
# Step 2: Iterate over the dictionary and filter B based on dict[i]
for key, array in bridge_sum_DNF.items():
    filtered_sublists = [sublist for sublist in bridge_sum_merged if sublist not in array]
    filtered_sublists = [invert(sublist) for sublist in filtered_sublists]
    bridge_sum_CNF[key] = filtered_sublists  # Replace dict[i] with filtered sublists

# Display the updated dictionary

for i in range(1,9):
    print(f"bridge_sum_CNF[{i}]=[", end=' ')
    for clause in bridge_sum_CNF[i]:
        print('[', end=' ')
        print(*clause, sep=", ", end=' ')
        print('], ', end=' ')
    print(']')
    
#node.val = 3 => bridge_sum[3] = [[],[], ]
#node.val = 3 => -[0] and -[1] and ... except 3 and -[8] Not(DNF) And Not(DNF) == CNF
