# This file is for parsing the input files

def parse_input_field(input_no):
    # Gets game field from input .txt file and sets the size of the game.
    # References global num in the main.

    # Opens the file, reads everything. Prints a list. Since the first two numbers always indicate
    # x and y size, sets these manually. Creates a list with all the islands, their locations and
    # the number of bridges.

    file = f'C:/Users/lutfu/Documents/group-k-sat-solving/Project_1/test{input_no}.txt'  # Parametrized input file selection
    contents = []  # Initializes contents of the field as a list

    with open(file) as t:
        size_info = t.readline().split()  # Gets rid of the of spaces for the x and y value in the input.
        x_size = int(size_info[0])  # X and Y value will always be at 0th and 1st position.
        y_size = int(size_info[1])

        print(f"Dimensions are {x_size}, {y_size}\n")  # Test print for internal usage. DELETE LATER
        contents = t.readlines()
        for line in contents:
            line.strip()
    return x_size, y_size, contents




