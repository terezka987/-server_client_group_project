# from tkinter import *
# from tkinter import ttk

# root = Tk()

import tkinter as tk

window = tk.Tk()
greeting = tk.Label(
    text="Hi, Pete",
    fg="purple",
    bg="pink",
    width=10,
    height=10
)

button = tk.Button(
    text="ok",
    anchor="w",
    width=8,
    height=2
)

entry = tk.Entry(fg="blue", bg="purple", width = 4)
https://realpython.com/python-gui-tkinter/#adding-a-widget

button.pack()
greeting.pack()
window.mainloop()
