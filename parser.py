# This file is for parsing the input files

def get_game_field():
    with open('test1.txt') as t:
        contents = t.readlines()
        print(contents)

        x_size = int(contents[0][0])
        y_size = int(contents[0][2])
        island_location = list()

        for i in range(1, x_size + 1):
            for j in range(y_size):
                if contents[i][j] != '.':
                    island_location.append((i, j, int(contents[i][j])))

    print(x_size, y_size)
    print(island_location)

    return x_size, y_size, island_location


def field_initialization(x_size, y_size, island_location):

    field = [[] * x_size for i in [] * y_size]


    elem = 0
    for i in range(0, len(island_location)):
        for j in range(2):
            field[i][j] = island_location[elem][2]
            elem += 1

    for i in range(0, len(field)):
        print(field[i])




def main():
    field_info = get_game_field()
    field_initialization(x_size=field_info[0], y_size=field_info[1], island_location=field_info[2])


if __name__ == "__main__":
    main()
