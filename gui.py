import random
import tkinter as tk
from tkinter import messagebox
from tkinter import font
import os
import main
from random import randint
from math import floor

input_no = 1
rows = []
cols = []
entry_grid = []
X_OFFSET = 40


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
            entry.grid(row=i + 6, column=j,sticky="NSEW")
            entry.insert(tk.END, '.')
            cols.append(entry.get())
            grid[i][j] = entry
        rows.append(cols)
    instructions_label = tk.Label(root,
                                  text="Please make sure to only enter valid island distributions! \n"
                                  "I.e. adjacent islands cannot exist.")
    instructions_label.grid(row=x + X_OFFSET, column=0, columnspan=3, padx=1, pady=1,sticky="NSEW")

    txt_button = tk.Button(root,
                           text="Save values and create grid.",
                           command=lambda: save_x_y_to_txt())
    txt_button.grid(row=x+X_OFFSET*2, column=0, columnspan=2, rowspan=1, sticky="NSEW")
    entry_grid = grid
    root.pack_slaves()
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
    run_button.grid(row=x + X_OFFSET*3, column=0, columnspan=2, rowspan=1, sticky="NSEW")
    root.pack_slaves()


def run_solver():
    global entry_grid
    global input_no
    main.main(True, input_no)
    messagebox.showinfo(
        "Ran Solver!", "You've ran the solver. Please check the Solution folder to see the result!")
    start_again_button = tk.Button(root,
                                   text="Start over?",
                                   command=clear)
    start_again_button.grid(row=int(entry_x.get())+X_OFFSET*4,
                            column=0, columnspan=2, rowspan=1, sticky="NSEW")
    input_no += 1
    root.pack_slaves()


def clear():
    for i in range(15, int(entry_x.get())+X_OFFSET*5):
        todeletelist = root.grid_slaves(row=i)
        for elem in todeletelist:
            elem.destroy()


# def generate_puzzle():
    # random_x_size = randint(3, 15)
    # random_y_size = randint(3, 15)
    # random_array = [[-1 for y in range(random_y_size + 2)]
    #                  for x in range(random_x_size + 2)]  # Create random 2d array

    # for i in range(1, random_x_size + 1):
    #      for j in range(1, random_y_size + 1):
    #          random_array[i][j] = 0

    # x = randint(1, random_x_size-1)
    # y = randint(1, random_y_size-1)
    # rand_island = (x, y, 1)

    # random_array[x + 1][y + 1] = 1
    # dir = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    # def build(x, y, grid, bridge, prev_dir, built):
    #     if built == 0:
    #         return None
    #     if x > len(grid) - 1 or y > len(grid) - 1 or x < 1 or y < 1:
    #         return False
    #     if grid[x][y] == 9 or grid[x][y] == 10:
    #         return False

    #     copy_dir = copy.deepcopy(dir)
    #     random.shuffle(copy_dir)

    #     action = randint(1, 2)  # 1 == build 2 == cont

    #     if ((action == 1 and not (1 <= grid[x-1][y] <=8 or 1 <= grid[x][y-1] <=8 or 1 <= grid[x+1][y] <=8 or 1 <= grid[x][y+1] <=8)) or grid[x][y] != 0):
    #         try_bridge = randint(9, 10)
    #         grid[x][y] += bridge % 4
    #         while (len(copy_dir) > 0):
    #             if action == 1:
    #                 if (build(x + copy_dir[0][0], y + copy_dir[0][1],
    #                         grid, try_bridge, copy_dir[0], built-1) == False):
    #                     grid[x][y] -= bridge % 4
    #                     copy_dir.remove(copy_dir[0])
    #                 else:
    #                     grid[x][y] += try_bridge % 4
    #                     return None
    #             else:
    #                 if (build(x + copy_dir[0][0], y + copy_dir[0][1],
    #                         grid, try_bridge, copy_dir[0], built) == False):
    #                     grid[x][y] -= bridge % 4
    #                     copy_dir.remove(copy_dir[0])
    #                 else:
    #                     grid[x][y] += try_bridge % 4
    #                     return None
                    

    #     else:
    #         grid[x][y] = bridge
    #         if (build(x + prev_dir[0], y + prev_dir[1], grid, bridge, prev_dir, built) == False):
    #             grid[x][y] = 0
    #             return False
            
    # while(len(dir) > 0):
    #     if (build(x + dir[0][0], y + dir[0][1],
    #     random_array, randint(9, 10), dir[0], 5)) == False:
    #         dir.remove(dir[0])
    #     else:
    #         break

    # for i in range(0, len(random_array)):
    #      print(f'{random_array[i]}\n')
    # print(rand_island)

root = tk.Tk()
root.title("Group K")
width = root.winfo_screenwidth() / 2
height = root.winfo_screenheight() / 4
screenquarterheight = height / 2
root.geometry(
    f'{int(width)}x{int(height)}+{int(width)}+{int(screenquarterheight)}')
root.columnconfigure(0, weight=1)
root.rowconfigure(6, weight=1)
default_font = font.nametofont("TkDefaultFont")
default_font.config(family="Arial",
                    size=10)

label_x = tk.Label(root, text="X Value")
entry_x = tk.Entry(root)
label_y = tk.Label(root, text="Y Value")
entry_y = tk.Entry(root)

confirm_button = tk.Button(root, text="Confirm",
                           command=save_values,
                           padx=2, pady=2, )

random_gen_button = tk.Button(root, text="Generate Random Puzzle",
                              padx=2, pady=2)


label_x.grid(row=0, column=0, rowspan=2, columnspan=1, sticky="NSEW")
entry_x.grid(row=0, column=1, rowspan=2, columnspan=1, sticky="NSEW")
label_y.grid(row=4, column=0, rowspan=2, columnspan=1, sticky="NSEW")
entry_y.grid(row=4, column=1, rowspan=2, columnspan=1, sticky="NSEW")
confirm_button.grid(row=0, column=3, columnspan=2, padx=1, pady=1, rowspan=1)
random_gen_button.grid(row=4, column=3, columnspan=2,
                       rowspan=1, padx=1, pady=1)
root.pack_slaves()
root.mainloop()
