from window import Window
import glob
import sys
import os


class RectSelector:

    def __init__(self, image_list, target_dir):
        # select a directory loaded.
        self._create_rect_selector()

    def _create_rect_selector(self):
        self._window = Window()


def main():
    _dir = sys.argv[1]
    path = _dir + '/*.jpg'
    image_list = [jpgFile for jpgFile in glob.glob(path)]
    target_dir = sys.argv[2]
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    RectSelector(image_list, target_dir)


if __name__ == '__main__':
    main()
