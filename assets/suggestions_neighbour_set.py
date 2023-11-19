grid = [
    [0, 2, 0, 3],
    [4, 5, 6, 0],
    [7, 0, 9, 10]
]

non_zero_elements = {}  # Dictionary to store non-zero elements and their positions

#WE PROBABLY WANT non_zero_elements to be a set since we can already access an element value through our field, so the mapping (i, j) -> value is unnecessary

# Store non-zero elements and their positions
for i, row in enumerate(grid):
    for j, value in enumerate(row):
        if value != 0:
            non_zero_elements[(i, j)] = value

# Function to find closest neighbors of a non-zero element
def find_closest_neighbors(position):
    x, y = position
    closest_neighbors = []
    
    # Check right
    for dy in range(1, len(grid[0]) - y):
        neighbor = (x, y + dy)
        if neighbor in non_zero_elements:
            closest_neighbors.append(neighbor)
            break
    
    # Check left
    for dy in range(1, y + 1):
        neighbor = (x, y - dy)
        if neighbor in non_zero_elements:
            closest_neighbors.append(neighbor)
            break
    
    # Check down
    for dx in range(1, len(grid) - x):
        neighbor = (x + dx, y)
        if neighbor in non_zero_elements:
            closest_neighbors.append(neighbor)
            break
    
    # Check up
    for dx in range(1, x + 1):
        neighbor = (x - dx, y)
        if neighbor in non_zero_elements:
            closest_neighbors.append(neighbor)
            break
    
    return closest_neighbors[:4]  # Return a maximum of 4 closest neighbors

# Iterate over non-zero elements and find their closest neighbors
for position in non_zero_elements:
    closest_neighbors = find_closest_neighbors(position)
    value = non_zero_elements[position]
    print(f"Element {value} at {position} has closest neighbors at: {closest_neighbors}")
