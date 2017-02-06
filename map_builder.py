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

        self._drag_data = {"x": 0, "y": 0, "item": None}

        self.canvas.tag_bind("piece", "<ButtonPress-1>", self.on_piece_press)
        self.canvas.tag_bind("piece", "<B1-Motion>", self.on_piece_motion)
        self.canvas.tag_bind("piece", "<ButtonRelease-1>",
                             self.on_piece_release)

    def open_image(self, file_path):
        img = Image.open(file_path)
        # Must bind it to the class in order to avoid it being garbage
        # collected
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(250, 250, image=self.tk_image, tags="piece")

    def on_piece_press(self, event):
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        print("Captured data: {}".format(self._drag_data))

    def on_piece_motion(self, event):
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]

        print("Computed delta {x}, {y}".format(x=delta_x, y=delta_y))

        self.canvas.move(self._drag_data["item"], delta_x, delta_y)

        print("Re-assigning drag data")
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_piece_release(self, event):
        print("Mouse button released, resetting drag data")
        self._drag_data = {"x": 0, "y": 0, "item": None}


if __name__ == '__main__':
    root = tk.Tk()
    cf = CanvasFrame(root)
    cf.pack(fill="both", expand=True)
    cf.open_image("test.png")
    root.mainloop()
