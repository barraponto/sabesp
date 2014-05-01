from PIL import Image, ImageFilter
from pyocr import tesseract


class SabespReader(object):

    @staticmethod
    def optimizer(image):
        return image.resize(
            [n*10 for n in image.size], Image.ANTIALIAS
        ).filter(
            ImageFilter.UnsharpMask(radius=16)
        ).convert(
            'P', palette=Image.ADAPTIVE, colors=2
        )

    def __init__(self, cropper):
        self.cropper = cropper

    def read(self):
        self.regions = {name: SabespReader.optimizer(region)
                        for name, region in self.cropper.regions.iteritems()}
        self.values = {name: tesseract.image_to_string(region)
                       for name, region in self.regions.iteritems()}
        return self.values
