import re
from PIL import Image, ImageFilter
from pyocr import tesseract
from unidecode import unidecode


class SabespReader(object):

    @staticmethod
    def image_optimizer(image, radius):
        return image.resize(
            [n*10 for n in image.size], Image.ANTIALIAS
        ).filter(
            ImageFilter.UnsharpMask(radius=radius)
        ).convert(
            'P', palette=Image.ADAPTIVE, colors=2
        )

    @staticmethod
    def text_optimizer(text):
        text = unidecode(text).replace(' ', '')
        text = text.replace(',', '.').replace('-', '.').replace('?', '7')
        search = re.compile(r'\d+\.\d+').findall(text)
        return search.pop() if search else False

    def read(self, name, region, radius=14):
        cls = type(self)
        txt = tesseract.image_to_string(
            cls.image_optimizer(self.cropper.regions[name], radius))
        try:
            return float(cls.text_optimizer(txt))
        except ValueError:
            return self.read(name, region, radius + 2) if radius < 21 else False

    def __init__(self, cropper):
        self.cropper = cropper
        self.values = {name: self.read(name, region)
                       for name, region in self.cropper.regions.iteritems()}
