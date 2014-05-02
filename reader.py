import re
from PIL import Image, ImageFilter
from pyocr import tesseract
from unidecode import unidecode


class SabespReader(object):

    @staticmethod
    def image_optimizer(image):
        return image.resize(
            [n*10 for n in image.size], Image.ANTIALIAS
        ).filter(
            ImageFilter.UnsharpMask(radius=14)
        ).convert(
            'P', palette=Image.ADAPTIVE, colors=2
        )

    @staticmethod
    def text_optimizer(text):
        text = unidecode(text).replace(' ', '')
        text = text.replace(',', '.').replace('-', '.').replace('?', '7')
        search = re.compile(r'\d+\.\d+').findall(text)
        return search.pop() if search else 'DEBUG ' + text

    def __init__(self, cropper):
        self.cropper = cropper
        self.regions = ((name, SabespReader.image_optimizer(region))
                        for name, region in self.cropper.regions.iteritems())
        self.values = {name: tesseract.image_to_string(region)
                       for name, region in self.regions}
        self.optivalues = {name: float(SabespReader.text_optimizer(text))
                           for name, text in self.values.iteritems()}
