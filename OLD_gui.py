import tkinter
from tkinter import *
#import parser

rows = []
for i in range(5):
    cols= []
    for j in range(5):
        e = Entry(relief=RIDGE)
        e.grid(row=i, column = j, sticky=NSEW)
        e.insert(END, '%d.%d' % (i, j))
        cols.append(e)
    rows.append(cols)

master = tkinter.Tk()
tkinter.Label(master, text="Number of columns").grid(row=0)
tkinter.Label(master, text="Number of rows").grid(row=1)

e_x = tkinter.Entry(master)
e_y = tkinter.Entry(master)

e_x.grid(row=0, column=1)
e_y.grid(row=1, column=1)

master.mainloop()

def onPress():
    for row in rows:
        for col in cols:
            print(col.get()),
        print()

Button(text='Fetch', command=onPress).grid()
mainloop()
