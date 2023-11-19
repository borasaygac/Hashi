grid = [
    [0, 2, 0, 3],
    [4, 5, 6, 0],
    [7, 0, 9, 10]
]

neighbours = {}  # Dictionary to store non-zero elements and their positions

#WE PROBABLY WANT non_zero_elements to be a set since we can already access an element value through our field, so the mapping (i, j) -> value is unnecessary

# Store non-zero elements and their positions
for i, row in enumerate(grid):
    for j, value in enumerate(row):
        if value != 0:
            neighbours[(i, j)] = []
print(neighbours)
# Function to find closest neighbors of a non-zero element
def find_closest_neighbors(position):
    x, y = position
    closest_neighbors = []
    print(f"x,y: {x}, {y}")
    # Check right
    for dy in range(1, len(grid[0]) - y):
        neighbor = (x, y + dy)
        if neighbor in neighbours:
            closest_neighbors.append(neighbor)
            break
        else:
            if (dy == (len(grid[0]) - y - 1)) | (y == (len(grid[0]) - 1)):
                closest_neighbors.append(None)
    
    # Check left
    for dy in range(1, y + 1):
        neighbor = (x, y - dy)
        if neighbor in neighbours:
            closest_neighbors.append(neighbor)
            break
        else:
            if (dy == y) | (y == 0):
                closest_neighbors.append(None)
    
    # Check down
    for dx in range(1, len(grid) - x):
        neighbor = (x + dx, y)
        if neighbor in neighbours:
            closest_neighbors.append(neighbor)
            break
        else:
            if (dx == (len(grid) - x - 1)) | (x == (len(grid) - 1)) :
                closest_neighbors.append(None)
        
    
    # Check up
    for dx in range(1, x + 1):
        neighbor = (x - dx, y)
        if neighbor in neighbours:
            closest_neighbors.append(neighbor)
            break
        else:
            if (dx == x) | ( x == 0 ):
                closest_neighbors.append(None)    
    
    return closest_neighbors  # Return a maximum of 4 closest neighbors

# Iterate over non-zero elements and find their closest neighbors
for position in neighbours:
    closest_neighbors = find_closest_neighbors(position)
    neighbours[position] = closest_neighbors
    print(f"Element {position} has closest neighbors at: {neighbours[position]}")
