import tkinter as tk
from tkinter import filedialog

root = tk.Tk()

root.geometry("500x500")
root.title("GROUP K")
#for some reasons it doesnt set the background to white even tough it should
root.configure(background='white')


#label
label = tk.Label(root, text="please select a file")
label.pack()

#after clicking the button this command is triggered
def select_file():
    filename = filedialog.askopenfilename()
    print(f'File selected: {filename}')

#button to select a file from the system
button = tk.Button(root, text="Select File", command=select_file)
button.pack(padx=50, pady=50)




root.mainloop()
