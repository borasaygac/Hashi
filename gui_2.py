import tkinter as tk
from tkinter import messagebox
import os

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
            entry.grid(row=i + 3, column=j)
            entry.insert(tk.END, '0')
            cols.append(entry.get())
            grid[i][j] = entry
        rows.append(cols)
    txt_button = tk.Button(root,
                           text="Save values and create grid.",
                           command=lambda: save_x_y_to_txt())
    txt_button.grid(row=x+4, column=0, columnspan=2, rowspan=1)
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
                if (j % (len(entry_grid[0])-1) == 0) & (j != 0):
                    file.write(f'{int(value)}\n')
                else:
                    file.write(f'{int(value)} ')

    run_button = tk.Button(root,
                           text="Run Solver!",
                           command=run_solver)
    run_button.grid(row=x + 5, column=0, columnspan=2, rowspan=1)


def run_solver():
    global entry_grid
    global input_no
    # main(True, input_no)
    messagebox.showinfo("Ran Solver!", "You've ran the solver. Please check the Solution folder to see the result!")
    start_again_button = tk.Button(root,
                                   text="Start over?",
                                   command=clear)
    start_again_button.grid(row=int(entry_x.get())+6, column=0, columnspan=2, rowspan=1)
    input_no += 1


def clear():
    for i in range(3, int(entry_x.get())+7):
        todeletelist = root.grid_slaves(row=i)
        for elem in todeletelist:
            elem.destroy()






root = tk.Tk()
root.title("Group K")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))  # Make it fullscreen with the os menu attached.
root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=0)

label_x = tk.Label(root, text="X Value")
entry_x = tk.Entry(root)
label_y = tk.Label(root, text="Y Value")
entry_y = tk.Entry(root)

button = tk.Button(root, text="Confirm",
                   command=save_values,
                   padx=2, pady=1)


label_x.grid(row=0, column=0)
entry_x.grid(row=0, column=1)
label_y.grid(row=1, column=0)
entry_y.grid(row=1, column=1)
button.grid(row=2)

root.mainloop()
