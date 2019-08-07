import os.path

import PIL
from PIL import Image
from PIL import ImageEnhance


class PillowAppEngine(object):

    """
    Implements a wrapper over the core Pillow functionality.
    Provides state and methods for UIs and other client
    software to streamline Pillow usage.
    """

    PILLOW_VERSION = PIL.__version__

    def __init__(self, on_image_change):

        self.image = None
        self._image_stack = []
        self._image_stack_index = None
        self._max_stack_size = 5
        self._undo_count = 0

        self.filepath = None
        self.saved = None
        self.on_image_change = on_image_change


    def open(self, filepath):

        """
        Attempts to create a Pillow Image from
        the filepath. If successful this becomes
        the "image" attribute.
        """

        try:
            image = Image.open(filepath)
            self.filepath = filepath
            self.saved = True
            self.__clear_stack()
            self.__add_to_stack(image)
            self.on_image_change()
        except Exception as e:
            self.__clear_stack()
            self.filepath = None
            raise


    def save(self, quality):

        """
        Attempts to save the image with the
        filename it was opened from.
        """

        try:
            self.image.save(self.filepath, quality=quality)
            self.saved = True
            self.on_image_change()
        except Exception as e:
            self.saved = False
            raise


    def save_as(self, filepath, quality):

        """
        Attempts to save the image to the
        specified filepath.
        """

        try:
            self.filepath = filepath
            self.image.save(self.filepath, quality=quality)
            self.saved = True
            self.on_image_change()
        except Exception as e:
            self.saved = False
            raise

    def close(self):

        """
        Sets the image other attributes to None.
        """

        self.image = None
        self.filepath = None
        self.saved = None
        self.__clear_stack()
        self.on_image_change()


    def __clear_stack(self):

        self._image_stack.clear()
        self._image_stack_index = None
        self.image = None


    def __add_to_stack(self, image):

        if self._image_stack_index is None:
            self._image_stack.append(image)
            self._image_stack_index = 0
        else:
            self._image_stack_index += 1
            self._image_stack.insert(self._image_stack_index, image)

        self.image = image

        # Images in stack after current no longer needed for redo
        del self._image_stack[self._image_stack_index+1:]

        # If stack is larger than maximum remove first
        if len(self._image_stack) > self._max_stack_size:
            del self._image_stack[0]

        self._undo_count = 0


    def undoable(self):

        if len(self._image_stack) > 1 and self._image_stack_index > 0:
            return True
        else:
            return False


    def redoable(self):
        if self._undo_count > 0:
            return True
        else:
            return False


    def undo(self):

        if self.undoable():
            self._undo_count += 1
            self._image_stack_index -= 1
            self.image = self._image_stack[self._image_stack_index]

            self.on_image_change()


    def redo(self):
        if self.redoable():
            self._image_stack_index += 1
            self.image = self._image_stack[self._image_stack_index]
            self._undo_count -= 1
            self.on_image_change()


    def get_properties(self):

        """
        Returns a dictionary containing various
        pieces of information on the image.
        """

        if self.image is not None:

            return {"filepath": self.filepath,
                    "filename": os.path.split(self.filepath)[1],
                    "width": self.image.width,
                    "height": self.image.height,
                    "format": self.image.format,
                    "mode": self.image.mode}

        else:

            return None


    def get_properties_text(self):

        """
        Returns the image information from
        get_properties in a text format.
        """

        if self.image is not None:

            properties = self.get_properties()

            format_string = "File Name: {}\nWidth:     {}\nHeight:    {}\nFormat:    {}\nMode:      {}"

            properties_text = format_string.format(properties["filename"],
                                                   properties["width"],
                                                   properties["height"],
                                                   properties["format"],
                                                   properties["mode"])

            return properties_text

        else:

            return "No image"


    def resize(self, width, height):

        """
        Uses the Pillow resize method.
        """

        resized = self.image.resize((width, height))
        self.__add_to_stack(resized)
        self.saved = False
        self.on_image_change()
