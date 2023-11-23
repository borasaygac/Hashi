import tkinter as tk
from tkinter import messagebox
import os
import main
from random import randint
from math import floor

input_no = 1
rows = []
cols = []
entry_grid = []


def save_values():
    try:
        x_value = int(entry_x.get())
        y_value = int(entry_y.get())

        print("Current X Value:", x_value)
        print("Current Y Value:", y_value)
        create_grid(x_value, y_value)
    except ValueError:
        print("Please enter an integer value")


def create_grid(x, y):
    global entry_grid
    grid = [[None for _ in range(y)] for _ in range(x)]
    for i in range(0, x):
        for j in range(0, y):
            entry = tk.Entry(root)
            entry.grid(row=i + 10, column=j)
            entry.insert(tk.END, '.')
            cols.append(entry.get())
            grid[i][j] = entry
        rows.append(cols)
    txt_button = tk.Button(root,
                           text="Save values and create grid.",
                           command=lambda: save_x_y_to_txt())
    txt_button.grid(row=x+30, column=0, columnspan=2, rowspan=1)
    entry_grid = grid
    return grid


def save_x_y_to_txt():
    global entry_grid
    global input_no
    x = int(entry_x.get())
    y = int(entry_y.get())

    output_folder = os.path.join(os.getcwd(), 'Project_1')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, f'input_man{input_no}.txt')

    with open(output_path, 'w') as file:
        file.write(f'{x} {y}\n')
        for i in range(0, x):
            for j in range(0, y):
                value = entry_grid[i][j].get()
                if value != '.':
                    file.write(f'{int(value)}')
                else:
                    file.write('.')
                    
                if (j % (len(entry_grid[0])-1) == 0) & (j != 0):
                    file.write('\n')                    

    run_button = tk.Button(root,
                           text="Run Solver!",
                           command=run_solver)
    run_button.grid(row=x + 16, column=0, columnspan=2, rowspan=1)


def run_solver():
    global entry_grid
    global input_no
    main.main(True, input_no)
    messagebox.showinfo("Ran Solver!", "You've ran the solver. Please check the Solution folder to see the result!")
    start_again_button = tk.Button(root,
                                   text="Start over?",
                                   command=clear)
    start_again_button.grid(row=int(entry_x.get())+12, column=0, columnspan=2, rowspan=1)
    input_no += 1


def clear():
    for i in range(10, int(entry_x.get())+40):
        todeletelist = root.grid_slaves(row=i)
        for elem in todeletelist:
            elem.destroy()


def randomized_field():
    random_x_size = randint(3, 15)
    random_y_size = randint(3, 15)
    random_array = [[-1 for y in range(random_y_size + 2)] for x in range(random_x_size + 2)]  # Create random 2d array

    for i in range(1, random_x_size + 1):
        for j in range(1, random_y_size + 1):
            random_array[i][j] = 0

    x = randint(1, random_x_size-1)
    y = randint(1, random_y_size-1)
    bridge_no = randint(1, 8)

    rand_island = (x, y, bridge_no)

    random_array[x + 1][y + 1] = bridge_no

    dir = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    bridges = [9, 10]
    val = 0

    def build(x, y, grid, bridge, prev_dir):
        if x > len(grid) - 1 or y > len(grid) - 1 or x < 1 or y < 1:
            return
        if grid[x][y] == 9 or grid[x][y] == 10:
            return
        if grid[x][y] != 0:
            if val == -1:
                x -= dir[prev_dir][0]
                y -= dir[prev_dir][1]
                grid[x][y] -= bridge
            rand = randint(0, 3)
            grid[x][y] += bridge % 4
            val_tmp = build(x + dir[rand][0], y + dir[rand][1], grid, randint(9, 10), dir[rand])
            val_tmp = val
            return -1
        action = randint(1, 2)  # 1 == build 2 == cont
        if action == 1:
            rand = randint(0, 3)
            # Potential while here
            build(x + dir[rand][0], y + dir[rand][1], grid, randint(9, 10), dir[rand])
        else:
            grid[x][y] = bridge
            build(x + prev_dir[0], y + prev_dir[1], grid, bridge, prev_dir)
            grid[x][y] = 0

    first_random_dir = randint(0, 3)
    build(x + dir[first_random_dir][0], y + dir[first_random_dir][1],
          random_array, randint(9, 10), dir[first_random_dir])

    for i in range(0, len(random_array)):
        print(f'{random_array[i]}\n')

    print(dir[first_random_dir])
    print(rand_island)


root = tk.Tk()
root.title("Group K")
width = root.winfo_screenwidth() / 2
height = root.winfo_screenheight() / 2
screenquarterheight = height / 2
root.geometry(f'{int(width)}x{int(height)}+{int(width)}+{int(screenquarterheight)}')  # Make it fullscreen with the os menu attached.
root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=0)

label_x = tk.Label(root, text="X Value")
entry_x = tk.Entry(root)
label_y = tk.Label(root, text="Y Value")
entry_y = tk.Entry(root)

confirm_button = tk.Button(root, text="Confirm",
                           command=save_values,
                           padx=2, pady=2)

random_gen_button = tk.Button(root, text="Generate Puzzle",
                              command=randomized_field,
                              padx=2, pady=2)


label_x.grid(row=0, column=0, rowspan=4, columnspan=2)
entry_x.grid(row=0, column=5, rowspan=2)
label_y.grid(row=4, column=0, rowspan=4, columnspan=2)
entry_y.grid(row=4, column=5, rowspan=2, columnspan=2)
confirm_button.grid(row=9, column=5, columnspan=4)
random_gen_button.grid(row=0, column=9, columnspan=4, rowspan=2, padx=2, pady=2)

root.mainloop()
