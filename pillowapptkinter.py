from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import PIL.ImageTk

import pillowappengine
import resizedialog
import qualitydialog


class ApplicationWindow(Frame):

    """
    Create and configure a Tkinter window.
    Also creates a pillowappengine.PillowAppEngine
    object which this application provides
    a front end for.
    """

    def __init__(self, master=None):

        self.pae = pillowappengine.PillowAppEngine(self.on_image_change)
        self.tkinter_image = None
        self.version = "0.4"
        self.application_name = "Tkinter Pillow App {}".format(self.version)
        self.window = Tk()
        self.window.geometry("800x600")
        self.window.attributes('-zoomed', True)
        self.window.grid_propagate(False)
        self.icon = PhotoImage(file='icon.gif')
        self.window.tk.call('wm', 'iconphoto', self.window._w, self.icon)
        self.window.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.window.update()
        self.width = self.window.winfo_width()
        self.height = self.window.winfo_height()

        self.create_menu()
        self.create_widgets()
        self.set_window_title()

        self.window.mainloop()


    def on_image_change(self):

        """
        Called by the PillowAppEngine when any changes are made
        to the image, or when an image is opened or closed.
        Calls the necessary functions to update the UI.
        """

        self.show_image()
        self.set_image_canvas_size()
        self.show_info()
        self.set_window_title()


    def show_image(self):

        """
        Creates a PIL.ImageTk.PhotoImage and displays it in the UI.
        """

        if self.pae.image is not None:
            self.tkinter_image = PIL.ImageTk.PhotoImage(self.pae.image)
            self.image_canvas.create_image(0, 0, image=self.tkinter_image, anchor="nw")
            self.image_canvas.grid(row=0, column=0, padx=2, pady=2)


    def set_image_canvas_size(self):

        """
        Sets the size of the canvas to that of the image.
        If this is larger than the parent window scrollbars
        will be enabled, so scrollregion needs to be set.
        """

        if self.tkinter_image is not None:
            self.window.update()
            w = self.tkinter_image.width()
            h = self.tkinter_image.height()
            self.image_canvas.config(width=w, height=h, scrollregion=(0, 0, w, h))


    def show_info(self):

        """
        Sets the image data in the panel if an image is open,
        or sets data to empty strings if there is no image.
        """

        if self.pae.image != None:
            info = self.pae.get_properties()
            self.filename_text.config(text=info["filename"])
            self.width_text.config(text=info["width"])
            self.height_text.config(text=info["height"])
            self.format_text.config(text=info["format"])
            self.mode_text.config(text=info["mode"])

            if self.pae.saved == True:
                self.saved_text.config(text="Yes")
            else:
                self.saved_text.config(text="No")

        else:
            self.filename_text.config(text="")
            self.width_text.config(text="")
            self.height_text.config(text="")
            self.format_text.config(text="")
            self.mode_text.config(text="")


    def set_window_title(self):

        """
        Shows just the application name if no image is open,
        or the application name and filename if an image is open.
        """

        if self.pae.image != None:
            title = self.application_name + ": " + self.pae.get_properties()["filename"]
            if self.pae.saved == False:
                title += "*"
            self.window.title(title)
        else:
            self.window.title(self.application_name)


    def on_quit(self):

        """
        Checks for any unsaved changes, then closes the application.
        """

        self.prompt_to_save()

        self.window.destroy()


    def on_resize(self, event):

        """
        Updates the object's width and height attributes
        """

        self.window.update()

        if self.window.winfo_width() != self.width or self.window.winfo_height() != self.height:
            self.width = self.window.winfo_width()
            self.height = self.window.winfo_height()


    def create_menu(self):

        """
        Creates the menu and sets event handlers.
        """

        menu = Menu(self.window)

        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open...", command=self.open)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_command(label="Save as...", command=self.save_as)
        filemenu.add_command(label="Close", command=self.close)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.on_quit)

        editmenu = Menu(menu)
        menu.add_cascade(label="Edit", menu=editmenu)
        editmenu.add_command(label="Undo", command=self.undo)
        editmenu.add_command(label="Redo", command=self.redo)

        imagemenu = Menu(menu)
        menu.add_cascade(label="Image", menu=imagemenu)
        imagemenu.add_command(label="Resize", command=self.resize)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.about)

        self.window.config(menu=menu)


    def create_widgets(self):

        """
        Creates all other components of the UI.
        """

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.toolbar = Frame(self.window, borderwidth=1, relief="raised")
        self.toolbar.grid(row=0, column=0, padx=0, pady=0, sticky=W+E)

        self.open_button = Button(self.toolbar, text="Open", command=self.open)
        self.open_button.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.open_graphic = PhotoImage(file="open.png")
        self.open_button.config(image=self.open_graphic, width="26", height="26")

        self.save_button = Button(self.toolbar, text="Save", command=self.save)
        self.save_button.grid(row=0, column=1, padx=2, pady=2, sticky=W)
        self.save_graphic = PhotoImage(file="save.png")
        self.save_button.config(image=self.save_graphic, width="26", height="26")

        self.undo_button = Button(self.toolbar, text="Undo", command=self.undo)
        self.undo_button.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.undo_graphic = PhotoImage(file="undo.png")
        self.undo_button.config(image=self.undo_graphic, width="26", height="26")

        self.redo_button = Button(self.toolbar, text="Redo", command=self.redo)
        self.redo_button.grid(row=0, column=3, padx=2, pady=2, sticky=W)
        self.redo_graphic = PhotoImage(file="redo.png")
        self.redo_button.config(image=self.redo_graphic, width="26", height="26")

        self.help_button = Button(self.toolbar, text="Help", command=self.about)
        self.help_button.grid(row=0, column=4, padx=2, pady=2, sticky=W)
        self.help_graphic = PhotoImage(file="info.png")
        self.help_button.config(image=self.help_graphic, width="26", height="26")

        self.image_frame = Frame(self.window, bg="white")
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid(row=1, column=0, padx=0, pady=0, sticky=W+E+N+S)

        self.hscroll = Scrollbar(self.image_frame, orient='horizontal')
        self.hscroll.grid(row=1, column=0, sticky=E+W)

        self.vscroll = Scrollbar(self.image_frame, orient='vertical')
        self.vscroll.grid(row=0, column=1, sticky=N+S)

        self.image_canvas = Canvas(self.image_frame, image=None, xscrollcommand=self.hscroll.set, yscrollcommand=self.vscroll.set)

        self.hscroll.config(command=self.image_canvas.xview)
        self.vscroll.config(command=self.image_canvas.yview)

        self.infobar = Frame(self.window, borderwidth=1, relief="raised")
        self.infobar.grid(row=2, column=0, padx=0, pady=0, sticky=W+E)

        self.filename_label = Label(self.infobar, text="Filename")
        self.filename_label.grid(row=0, column=0, padx=2, pady=2, sticky=W)

        self.filename_text = Label(self.infobar, bg="white", text="", borderwidth=1, relief="sunken", width=16, anchor="w")
        self.filename_text.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        self.saved_label = Label(self.infobar, text="Saved")
        self.saved_label.grid(row=0, column=2, padx=2, pady=2, sticky=W)

        self.saved_text = Label(self.infobar, bg="white", text="", borderwidth=1, relief="sunken", width=3, anchor="w")
        self.saved_text.grid(row=0, column=3, padx=2, pady=2, sticky=W)

        self.width_label = Label(self.infobar, text="Width")
        self.width_label.grid(row=0, column=4, padx=2, pady=2, sticky=W)

        self.width_text = Label(self.infobar, bg="white", text="", borderwidth=1, relief="sunken", width=5)
        self.width_text.grid(row=0, column=5, padx=2, pady=2, sticky=W)

        self.height_label = Label(self.infobar, text="Height")
        self.height_label.grid(row=0, column=6, padx=2, pady=2, sticky=W)

        self.height_text = Label(self.infobar, bg="white", text="", borderwidth=1, relief="sunken", width=5)
        self.height_text.grid(row=0, column=7, padx=2, pady=2, sticky=W)

        self.format_label = Label(self.infobar, text="Format")
        self.format_label.grid(row=0, column=8, padx=2, pady=2, sticky=W)

        self.format_text = Label(self.infobar, bg="white", text="", borderwidth=1, relief="sunken", width=5)
        self.format_text.grid(row=0, column=9, padx=2, pady=2, sticky=W)

        self.mode_label = Label(self.infobar, text="Mode")
        self.mode_label.grid(row=0, column=10, padx=2, pady=2, sticky=W)

        self.mode_text = Label(self.infobar, bg="white", text="", borderwidth=1, relief="sunken", width=5)
        self.mode_text.grid(row=0, column=11, padx=2, pady=2, sticky=W)

        self.window.bind("<Configure>", self.on_resize)


    def about(self):

        """
        Shows a message box containing application information.
        """

        about_text = "CodeDrome\ncodedrome.com\n\n{}\n\nUsing Pillow {}"
        about_text = about_text.format(self.application_name,
        pillowappengine.PillowAppEngine.PILLOW_VERSION)
        messagebox.showinfo('About', about_text)


    def open(self):

        """
        Used as an event handler for menu and toolbar button.
        """

        try:
            filepath = filedialog.askopenfilename(title="Open image", filetypes=(("JPEG files", "*.jpg"),))
            # Clicking Cancel returns an empty tuple.
            if filepath != ():
                self.pae.open(filepath)
        except Exception as e:
            self.show_error_message("Open", e)


    def save(self):

        """
        Used as an event handler for menu and toolbar button.
        """

        if self.pae.image is not None:
            try:
                quality = 75
                quality_dialog = qualitydialog.QualityDialog(quality)
                self.window.wait_window(quality_dialog.dlg)
                self.pae.save(quality_dialog.quality)
            except Exception as e:
                self.show_error_message("Save", e)


    def save_as(self):

        """
        Used as an event handler for menu.
        """

        try:
            filepath = filedialog.asksaveasfile(title="Save image as", filetypes=(("JPEG files", "*.jpg"),))
            # Clicking Cancel returns None.
            if filepath is not None:
                quality = 75
                quality_dialog = qualitydialog.QualityDialog(quality)
                self.window.wait_window(quality_dialog.dlg)
                self.pae.save_as(filepath.name, quality_dialog.quality)
        except Exception as e:
            self.show_error_message("Save as", e)


    def close(self):

        """
        Used as an event handler for menu.
        """

        self.prompt_to_save()

        self.pae.close()
        self.image_canvas.grid_forget()


    def undo(self):

        """
        Used as an event handler for menu/button.
        """

        self.pae.undo()


    def redo(self):

        """
        Used as an event handler for menu/button.
        """

        self.pae.redo()


    def resize(self):

        """
        Used as an event handler for menu.
        """

        info = self.pae.get_properties()
        # self.width_text.config(text=info["width"])
        # self.height_text.config(text=info["height"])

        new_dimensions = {"width": 0, "height": 0}
        current_dimensions = {"width": info["width"], "height": info["height"]}

        resize_dialog = resizedialog.ResizeDialog(current_dimensions, new_dimensions)
        self.window.wait_window(resize_dialog.dlg)

        if new_dimensions["width"] > 0 and new_dimensions["width"] > 0 :
            self.pae.resize(new_dimensions["width"], new_dimensions["height"])


    def show_error_message(self, title, e):

        messagebox.showerror(title, e)

    def prompt_to_save(self):

        if self.pae.saved == False:
            if messagebox.askyesno("Save changes", "Do you want to save changes?") == True:
                if self.pae.filepath is not None:
                    self.save()
                else:
                    self.save_as()


def main():
    appwin = ApplicationWindow()


main()
