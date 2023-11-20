def initialise_field(x_size, y_size, contents):
    initialised_field = [["." for x in range(y_size)] for y in
                         range(x_size)]  # Creates a 2D-Array all set with dots.

    for i in range(x_size):

        for j in range(y_size):

            # 2 for loops for checking each node.
            # Either a dot, or the number of bridges of an island, stored within contents.
            if contents[i][j] != '.':
                initialised_field[i][j] = int(contents[i][j])
            else:
                initialised_field[i][j] = contents[i][j]
                #V[1..n] = ..
                #H[1::m] = ..


    neighbours = {}  # Dictionary to store non-zero elements and their positions


    # Store non-zero elements and their positions
    for i, row in enumerate(initialised_field):
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
        if (y == len(initialised_field[0]) - 1):
            closest_neighbors.append(None)
        for dy in range(1, len(initialised_field[0]) - y):
            neighbor = (x, y + dy)
            if neighbor in neighbours:
                closest_neighbors.append(neighbor)
                break
            else:
                if dy == len(initialised_field[0]) - y - 1:
                    closest_neighbors.append(None)

        # Check left
        if (y == 0):
            closest_neighbors.append(None)
        for dy in range(1, y + 1):
            neighbor = (x, y - dy)
            if neighbor in neighbours:
                closest_neighbors.append(neighbor)
                break
            else:
                if (dy == y):
                    closest_neighbors.append(None)

        # Check down
        if (x == len(initialised_field) - 1):
            closest_neighbors.append(None)
        for dx in range(1, len(initialised_field) - x):
            neighbor = (x + dx, y)
            if neighbor in neighbours:
                closest_neighbors.append(neighbor)
                break
            else:
                if dx == len(initialised_field) - x - 1:
                    closest_neighbors.append(None)

        # Check up
        if (x == 0):
            closest_neighbors.append(None)
        for dx in range(1, x + 1):
            neighbor = (x - dx, y)
            if neighbor in neighbours:
                closest_neighbors.append(neighbor)
                break
            else:
                if (dx == x):
                    closest_neighbors.append(None)

        return closest_neighbors  # Return a maximum of 4 closest neighbors

    # Iterate over non-zero elements and find their closest neighbors
    for position in neighbours:
        closest_neighbors = find_closest_neighbors(position)
        neighbours[position] = closest_neighbors
        print(f"Element {position} has closest neighbors at: {neighbours[position]}")


    for row in initialised_field:  # Prints the 2d initialised_field for internal purposes. DELETE LATER.
        for element in row:
            print(element, end=' ')
        print("\n")
    return initialised_field
