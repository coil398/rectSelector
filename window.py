import tkinter


class Window:

    def __init__(self):
        root = tkinter.Tk()
        self._create_window(root)
        root.mainloop()

    def _create_window(self, root):
        pass

    def process_images(self, image_list, target_dir):
        pass
