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

    for row in initialised_field:  # Prints the 2d initialised_field for internal purposes. DELETE LATER.
        for element in row:
            print(element, end=' ')
        print("\n")
    return initialised_field
