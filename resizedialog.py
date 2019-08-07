from tkinter import *


class ResizeDialog(object):

    def __init__(self, current_dimensions, new_dimensions):

        self.new_dimensions = new_dimensions
        self.current_dimensions = current_dimensions

        self.dlg = Toplevel()

        self.dlg.title("Resize")

        self.dlg.grab_set()

        self.width_label = Label(self.dlg, text="Width")
        self.width_label.grid(row=0, column=0, padx=4, pady=4, sticky=W)

        self.width_box = Entry(self.dlg)
        self.width_box.insert(0, current_dimensions["width"])
        self.width_box.grid(row=0, column=1, padx=4, pady=4, sticky=W)

        self.calculate_width_button = Button(self.dlg, text='Calculate', command=self.calculate_width)
        self.calculate_width_button.grid(row=0, column=2, padx=4, pady=4, sticky=W)

        self.height_label = Label(self.dlg, text="Height")
        self.height_label.grid(row=1, column=0, padx=4, pady=4, sticky=W)

        self.height_box = Entry(self.dlg)
        self.height_box.insert(0, current_dimensions["height"])
        self.height_box.grid(row=1, column=1, padx=4, pady=4, sticky=W)

        self.calculate_height_button = Button(self.dlg, text='Calculate', command=self.calculate_height)
        self.calculate_height_button.grid(row=1, column=2, padx=4, pady=4, sticky=W)

        self.ok_button = Button(self.dlg, text='OK', command=self.ok)
        self.ok_button.grid(row=2, column=0, columnspan=3, padx=4, pady=4, sticky=W+E)

        self.cancel_button = Button(self.dlg, text='Cancel', command=self.cancel)
        self.cancel_button.grid(row=3, column=0, columnspan=3, padx=4, pady=4, sticky=W+E)


    def ok(self):

        width_valid = self.get_width()

        height_valid = self.get_height()

        if width_valid and height_valid:
            self.dlg.destroy()


    def cancel(self):

        self.new_dimensions["width"] = 0
        self.new_dimensions["height"] = 0

        self.dlg.destroy()

    def get_width(self):

        try:
            self.width_box.config(bg="white")
            self.new_dimensions["width"] = int(self.width_box.get())
            if self.new_dimensions["width"] <= 0:
                self.width_box.config(bg="yellow")
                return False
            else:
                return True
        except ValueError:
            self.width_box.config(bg="yellow")
            return False

    def get_height(self):

        try:
            self.height_box.config(bg="white")
            self.new_dimensions["height"] = int(self.height_box.get())
            if self.new_dimensions["height"] <= 0:
                self.height_box.config(bg="yellow")
                return False
            else:
                return True
        except ValueError:
            self.height_box.config(bg="yellow")
            return False

    def calculate_height(self):

        width_valid = self.get_width()

        if width_valid:
            h_w_ratio = self.current_dimensions["width"] / self.current_dimensions["height"]
            self.new_dimensions["height"] = int(self.new_dimensions["width"] / h_w_ratio)
            self.height_box.delete(0, "end")
            self.height_box.insert(0, self.new_dimensions["height"])


    def calculate_width(self):

        height_valid = self.get_height()

        if height_valid:
            h_w_ratio = self.current_dimensions["width"] / self.current_dimensions["height"]
            self.new_dimensions["width"] = int(self.new_dimensions["height"] * h_w_ratio)
            self.width_box.delete(0, "end")
            self.width_box.insert(0, self.new_dimensions["width"])
