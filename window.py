import tkinter
from PIL import Image, ImageTk
from collections import namedtuple
import os
import json


labels = ('Chino', 'Cocoa', 'Rize', 'Syaro', 'Chiya')
colors = ('blue', 'orange', 'purple', 'brown', 'yellow')
# RGB = namedtuple('RGB', ('red', 'green', 'blue'))
# colors = (RGB(228, 228, 240), RGB(238, 195, 161), RGB(94, 69, 109), RGB(89, 71, 71), RGB(247, 234, 190))
Rect = namedtuple('Rect', ('xmin', 'ymin', 'xmax', 'ymax'))
Sample = namedtuple('Sample', ['filename', 'boxes', 'imgsize'])
Box = namedtuple('Box', ['label', 'labelid', 'center', 'size'])

WIDTH_OF_CANVAS = 1752
HEIGHT_OF_CANVAS = 982


def namedtuple2tuple(namedtuple):
    res = [t for t in namedtuple]
    return tuple(res)


class PopupWindow:

    def __init__(self, parent, root, rect):
        self._parent = parent
        self._top = tkinter.Toplevel(root)
        self._rect = rect
        self._set_components()

    def _display_radiobuttons(self):
        for index, label in enumerate(labels):
            label = tkinter.Radiobutton(self._top, text=label, variable=self._variable, value=index)
            label.pack()

    def _display_send_button(self):
        button = tkinter.Button(self._top, text='submit', command=self._send_radiobutton)
        button.pack()

    def _set_components(self):
        self._variable = tkinter.IntVar()
        self._display_radiobuttons()
        self._display_send_button()

    def _send_radiobutton(self):
        status = self._variable.get()
        self._parent.add_rect(status, self._rect)
        self._top.destroy()


class Window:

    def __init__(self, _dir, image_list, target_dir):
        self._root = tkinter.Tk()
        # root.geometry('800x560')
        self._dir = _dir
        self._image_list = image_list
        self._target_dir = target_dir
        self._create_canvas(self._root)
        self._image_index = 0
        self._max_image_index = len(self._image_list) - 1

        self._min = set()
        self._rect_list = list()

        self._set_events(self._root)
        self._set_components(self._root)
        self._initialize()
        self._root.mainloop()

    def _initialize(self):
        if self._max_image_index == -1:
            import sys
            sys.exit()
        # image = Image.open(self._image_list[0])
        image = Image.open(self._image_list[0])
        self._canvas.image = ImageTk.PhotoImage(image)
        self._canvas.create_image(0, 0, image=self._canvas.image, anchor=tkinter.NW)

    def _del_rect_list(self):
        self._rect_list = list()

    def _create_rect(self, e):
        rect = Rect(self._min[0], self._min[1], e.x, e.y)
        popupWindow = PopupWindow(self, self._root, rect)

    def _display_rect(self, rect, status):
        self._canvas.create_rectangle(rect[0], rect[1], rect[2], rect[3], outline=colors[status])
        self._canvas.create_text(rect[0]+10, rect[1]-10, text=labels[status], fill=colors[status])

    def add_rect(self, status, rect):
        self._display_rect(rect, status)
        self._rect_list.append((rect, status))

    def _click_on_canvas(self, e):
        if not self._min:
            self._min = (e.x, e.y)

        else:
            self._create_rect(e)
            self._min = set()

    def _click_right_on_canvas(self, e):
        if self._min:
            self._min = set()
            self._canvas.delete('rect')

    def _move_on_canvas(self, e):
        if self._min:
            self._canvas.delete('rect')
            self._canvas.create_rectangle(self._min, e.x, e.y, tag='rect')

    def _set_events(self, root):
        self._canvas.bind('<Button-1>', self._click_on_canvas)
        self._canvas.bind('<Button-3>', self._click_right_on_canvas)
        self._canvas.bind('<Motion>', self._move_on_canvas)

    def _set_buttons(self, root):
        # next button
        self._next_button = tkinter.Button(root, text='Next', command=self._next_button, width=20, height=5)
        self._next_button.grid(row=0, column=2, columnspan=1, rowspan=1)

        # prev button
        self._prev_button = tkinter.Button(root, text='Prev', command=self._prev_button, width=20, height=5)
        self._prev_button.grid(row=1, column=2, columnspan=1, rowspan=1)

        # save button
        self._save_button = tkinter.Button(root, text='Save', command=self._save_button, width=20, height=5)
        self._save_button.grid(row=2, column=2, columnspan=1, rowspan=1)

    def _set_components(self, root):
        self._set_buttons(root)

    def _create_canvas(self, root):
        self._canvas = tkinter.Canvas(root, width=WIDTH_OF_CANVAS, height=HEIGHT_OF_CANVAS)
        self._canvas.grid(row=0, column=0, columnspan=2, rowspan=4)

    def _display_image(self, path):
        image = Image.open(path)
        self._canvas.image = ImageTk.PhotoImage(image)
        self._canvas.create_image(0, 0, image=self._canvas.image, anchor=tkinter.NW)

    def _next_button(self):
        if self._image_index == self._max_image_index:
            import sys
            sys.exit()
        self._image_index += 1
        self._display_image(self._image_list[self._image_index])
        self._del_rect_list()

    def _prev_button(self):
        if self._image_index == 0:
            return
        self._image_index -= 1
        self._display_image(self._image_list[self._image_index])
        self._reinitialize()

    def _save_button(self):
        data = dict()
        path = self._image_list[self._image_index].split('/')[1].split('.')[0]
        print(path)
        target_path = self._target_dir + '/' + path + '.json'
        data[path] = list()
        for rect in self._rect_list:
            data[path].append(rect)
        with open(target_path, 'w') as f:
            json.dump(data, f)
