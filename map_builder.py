#!/usr/bin/env python

from PIL import Image, ImageTk
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack()

img = Image.open("test.png")

tk_image = ImageTk.PhotoImage(img)

canvas.create_image(250, 250, image=tk_image)

root.mainloop()
