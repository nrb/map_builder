#!/usr/bin/env python

import os
from PIL import Image, ImageTk
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class CanvasFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        # Width will automatically fill to the frame, but height won't,
        # so we specify it.
        self.canvas = tk.Canvas(background="red",
                                height=1080)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Capture keyboard events
        self.focus_set()

        self._selection = None

        # Retain a handle to all loaded images
        self._images = []

        self._drag_data = {"x": 0, "y": 0, "item": None}

        self.canvas.tag_bind("piece", "<ButtonPress-1>", self.on_piece_press)
        self.canvas.tag_bind("piece", "<B1-Motion>", self.on_piece_motion)
        self.canvas.tag_bind("piece", "<ButtonRelease-1>",
                             self.on_piece_release)
        self.bind("<Delete>", self.on_delete)

    def open_image(self, file_path):
        img = Image.open(file_path)
        tk_image = ImageTk.PhotoImage(img)
        # Add the image to all the ones we're tracking on the canvas
        self._images.append(tk_image)
        self.canvas.create_image(250, 250, image=self._images[-1],
                                 tags="piece")

    def on_piece_press(self, event):
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]

        # Note: we're not worrying about doing ctrl-click stuff now,
        # maybe ever.
        if not self._selection:
            self._selection = self._drag_data["item"]
            print("Selection set.")
        # If this thing is already selected, de-select it
        elif self._selection == self._drag_data["item"]:
            self._selection = None
            print("Selection unset")
        # This clause could probably be merged into the first case,
        # but for now we'll leave it.
        elif not self._selection == self._drag_data["item"]:
            self._selection = self._drag_data["item"]
            print("Selection changed")

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

    def on_delete(self, event):
        print("Symbol was: {}".format(event.widget))

        if self._selection:
            self.canvas.delete(self._selection)
            self._selection = None
        else:
            print("Nothing selected.")


def get_file_names(resource_dir):
    files = os.listdir(resource_dir)

    return files


if __name__ == '__main__':
    root = tk.Tk()

    list_frame = tk.LabelFrame(root, text="Tiles", height=1080,
                               width=(1920 * 0.25))
    list_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)

    list_box = tk.Listbox(list_frame)
    list_box.pack(fill=tk.Y, expand=True)

    files = get_file_names('resources')

    for _file in files:
        list_box.insert(tk.END, _file)

    cf = CanvasFrame(root, height=1080, width=(1920 * 0.75))
    cf.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    cf.open_image("test.png")
    cf.open_image("test2.png")

    root.mainloop()
