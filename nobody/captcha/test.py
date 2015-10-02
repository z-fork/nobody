# -*- coding: utf-8 -*-

from PIL import Image
from PIL.ImageColor import getrgb


class Captcha(object):
    WHITE = getrgb('white')
    BLACK = getrgb('black')

    def __init__(self, path):
        self.img = Image.open(path).convert('RGB')
        self.pix = self.img.load()
        self.threshold = 21
        self.window = 2

    def prepare(self):
        # binarization
        width, height = self.img.size
        for x in xrange(width):
            for y in xrange(height):
                r, g, b = self.pix[x, y]
                if r > self.threshold or g > self.threshold or b > self.threshold:
                    self.pix[x, y] = self.WHITE
                else:
                    self.pix[x, y] = self.BLACK

    def noise(self):
        # 中值滤波
        if self.window == 1:
            window_x = [1, 0, 0, -1, 0]
            window_y = [0, 1, 0, 0, -1]
        elif self.window == 2:
            window_x = [-1, 0, 1, -1, 0, 1, 1, -1, 0]
            window_y = [-1, -1, -1, 1, 1, 1, 0, 0, 0]

        width, height = self.img.size

        for x in xrange(width):
            for y in xrange(height):
                box = []
                for i in xrange(len(window_x)):
                    d_x = x + window_x[i]
                    d_y = y + window_y[i]
                    try:
                        point = self.pix[d_x, d_y]
                        if point == self.BLACK:
                            box.append(1)
                        else:
                            box.append(0)
                    except IndexError:
                        self.pix[x, y] = self.WHITE
                        continue
                box.sort()
                if len(box) == len(window_x):
                    mid = box[len(box)/2]
                    if mid == 1:
                        self.pix[x, y] = self.BLACK
                    else:
                        self.pix[x, y] = self.WHITE

    def split(self):
        img_new = self.img.copy()
        pix_new = img_new.load()
        width, height = self.img.size
        line_status = None
        pos_x = []

        for x in xrange(width):
            pixs = []
            for y in xrange(height):
                pixs.append(self.pix[x, y])

            if len(set(pixs)) == 1:
                _line_status = 0
            else:
                _line_status = 1

            if _line_status != line_status:
                if _line_status == 0:
                    _x = x
                elif _line_status == 1:
                    _x = x - 1

                pos_x.append(_x)

                for _y in xrange(height):
                    pix_new[x, _y] = self.BLACK

            line_status = _line_status

        # img_new.show()
        # print pos_x

        i = 1
        divs = []
        boxs = []
        while True:
            try:
                xi = pos_x[i]
                xj = pos_x[i+1]
            except Exception:
                break
            i += 2
            boxs.append([xi, xj])

        # fixed_boxs = []
        # i = 0
        # while i < len(boxs):
        #     box = boxs[i]
        #     if box[1] - box[0] < 10:
        #         try:
        #             box_next = boxs[i+1]
        #             fixed_boxs.append([box[0], box_next[1]])
        #             i += 2
        #         except Exception:
        #             break
        #     else:
        #         fixed_boxs.append(box)
        #         i += 1
        fixed_boxs = boxs

        for box in fixed_boxs:
            div = self.img.crop((box[0], 0, box[1], height))
            try:
                # divs.append(format_div(div, size=(20, 40)))
                divs.append(div)
            except Exception:
                divs.append(div)

        _divs = []
        for div in divs:
            # width, height = div.size
            # if width < 5:
            #     continue

            # pix = div.load()
            # points = 0
            # for i in xrange(width):
            #     for j in xrange(height):
            #         p = pix[i, j]
            #         if p == self.BLACK:
            #             points += 1

            # if points <= 5:
            #     continue
            # new_div = format_div(div)
            new_div = div
            _divs.append(new_div)

        return _divs

    def show(self):
        self.img.show()

    @staticmethod
    def image_to_string(img, config='-psm 8'):
        import pytesseract
        try:
            # result = pytesseract.image_to_string(img, lang='eng', config=config)
            result = pytesseract.image_to_string(img, lang='eng', config='-psm 8')
            result = result.strip()
            return result.lower()
        except Exception:
            return None

c = Captcha('/Users/dinghailong/Downloads/relation.jpg')
c.prepare()
c.noise()

c.img.show()

# # for im in c.split():
# #     im.show()
# #     print c.image_to_string(im)
#
# print c.image_to_string(c.img)
#
#
# print '-' * 10
# im = Image.open('/Users/dinghailong/Downloads/1989.jpg')
# # im_big = im.resize((1000, 500), Image.NEAREST)
# import pytesseract
# try:
#     result = pytesseract.image_to_string(im, lang='eng', config='-psm 8')
#     print result
# except Exception:
#     print 'Not ...'
