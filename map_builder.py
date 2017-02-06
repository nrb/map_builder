#!/usr/bin/env python

from PIL import Image, ImageTk
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class CanvasFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(width=(1920 * 0.75), height=1080)
        self.canvas.pack(fill="both", expand=True)

    def open_image(self, file_path):
        img = Image.open(file_path)
        # Must bind it to the class in order to avoid it being garbage
        # collected
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(250, 250, image=self.tk_image)


if __name__ == '__main__':
    root = tk.Tk()
    cf = CanvasFrame(root)
    cf.pack(fill="both", expand=True)
    cf.open_image("test.png")
    root.mainloop()
