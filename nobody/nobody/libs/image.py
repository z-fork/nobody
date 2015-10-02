# -*- coding: utf-8 -*-

"""
    ImageConvert:  convert png, gif image to jpeg image.
    create_image: use buf create image.
"""
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from PIL import Image


class ImageConvert(object):

    @classmethod
    def _png_to_jpeg(cls, im):
        _im = create_image('JPEG', 'RGBA', im.size)
        _im.paste(im, im)
        _im = _im.convert('RGB')
        return _im

    @classmethod
    def _gif_to_jpeg(cls, im):
        _im = cls._gif_to_png(im)
        _im = cls._png_to_jpeg(_im)
        return _im

    @classmethod
    def _gif_to_png(cls, im):
        _im = create_image('PNG', 'RGBA', im.size)
        _im.paste(im)
        return _im

    @classmethod
    def convert(cls, im):
        if im.format == 'PNG' and im.mode == 'RGBA':
            im = cls._png_to_jpeg(im)
        elif im.format == 'GIF':
            im = cls._gif_to_jpeg(im)
        elif im.mode != 'RGB':
            im = im.convert('RGB')
        return im


def create_image(_format, *a, **kw):
    buf = StringIO()
    Image.new(*a, **kw).save(buf, _format)
    buf.seek(0)
    return Image.open(buf)
