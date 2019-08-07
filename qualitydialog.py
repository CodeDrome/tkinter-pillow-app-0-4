from tkinter import *


class QualityDialog(object):

    def __init__(self, quality):

        self.quality = quality

        self.dlg = Toplevel()

        self.dlg.title("Quality")

        self.dlg.grab_set()

        self.slider = Scale(self.dlg, from_=1, to=95, length=200, orient=HORIZONTAL)
        self.slider.set(quality)
        self.slider.grid(row=0, column=0, padx=4, pady=4, sticky=W)

        self.ok_button = Button(self.dlg, text='OK', command=self.ok)
        self.ok_button.grid(row=2, column=0, columnspan=3, padx=4, pady=4, sticky=W+E)


    def ok(self):

        self.quality = self.slider.get()

        self.dlg.destroy()
