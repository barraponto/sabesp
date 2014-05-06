from PIL import Image
from pyocr import tesseract


class CropperReader(object):
    ''' Gets data bits out of images.'''

    # This dict should hold region definitions in a tuple keyed by region name.
    # {region_name: (left, top, right, bottom)}
    regions = {}

    def __init__(self, filename):
        ''' Readies an image for data extraction.
        :param filename: a string representing the path to an image file.
        '''
        self.image = Image.open(filename)
        self.cropped_regions = {name: self.image.crop(coords)
                                for name, coords in self.regions.iteritems()}

    def read_image(self,
                   image_optimizer=None, data_optimizer=None, threshold=None):
        ''' Reads values for every defined region.
        For params documentation see CropperReader.get_data.
        '''
        self.values = {
            name: self.get_data(
                region, 0, image_optimizer, data_optimizer, threshold)
            for name, region in self.cropped_regions.iteritems()}
        return self

    def get_data(self, region, rerun=0,
                 image_optimizer=None, data_optimizer=None, threshold=None):
        '''Gets data out of a single region
        :param rerun: incrementing integer for every rerun.
        :param image_optimizer: callback, takes PIL.Image and rerun as params.
        :param data_optimizer: callback, takes String and rerun as params.
        :param threshold: callback, takes String and should return False for a rerun.
        '''
        if image_optimizer:
            region = image_optimizer(region, rerun)
        data = tesseract.image_to_string(region)
        if data_optimizer:
            data = data_optimizer(data, rerun)
        if threshold and not threshold(data):
            return self.get_data(
                self, region, rerun + 1,
                image_optimizer, data_optimizer, threshold)
        else:
            return data
