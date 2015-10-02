# -*- coding: utf-8 -*-

from StringIO import StringIO
import itertools

try:
    import Image
except ImportError:
    from PIL import Image
from PIL.ImageColor import getrgb
import pytesseract


class Captcha(object):
    WHITE = getrgb('white')
    BLACK = getrgb('black')

    def __init__(self, path=None, content=None):
        if content:
            self.img = Image.open(StringIO(content)).convert('RGB')
        else:
            self.img = Image.open(path).convert('RGB')

        self.is_binary = False
        self.is_denoise = False
        self.pix = self.img.load()
        self.threshold = 21

    def binarization(self):
        width, height = self.img.size
        for x, y in itertools.product(xrange(width), xrange(height)):
            r, g, b = self.pix[x, y]
            if r > self.threshold or g > self.threshold or b > self.threshold:
                self.pix[x, y] = self.WHITE
            else:
                self.pix[x, y] = self.BLACK

        self.is_binary = True

    def denoise(self, types=2):
        # 中值滤波
        windows = {
            1: [
                (1, 0), (0, 1), (0, 0), (-1, 0), (0, -1)
            ],
            2: [
                (-1, -1), (0, -1), (1, -1), (-1, 1),
                (0, 1), (1, 1), (1, 0), (-1, 0), (0, 0)
            ]
        }

        window = windows[types]
        width, height = self.img.size

        for x, y in itertools.product(xrange(width), xrange(height)):
            box = []
            for i, j in window:
                try:
                    box.append(1) if self.pix[x+i, y+j] == self.BLACK else box.append(0)
                except IndexError:
                    self.pix[x, y] = self.WHITE
            box.sort()
            if len(box) == len(window):
                mid = box[len(box)/2]
                self.pix[x, y] = self.BLACK if mid == 1 else self.WHITE

        self.is_denoise = True

    def image_to_string(self, lang='eng', config='-psm 8'):
        try:
            return pytesseract.image_to_string(self.img, lang=lang, config=config).strip().lower()
        except Exception:
            return None

    def to_string(self):
        self.binarization()
        self.denoise()
        return self.image_to_string()


if __name__ == "__main__":
    c = Captcha('/Users/dinghailong/Downloads/relation.jpg')
    print c.to_string()
