from PIL import Image


class SabespCropper(object):
    ''' Gets data bits out of Sabesp fugly reports.'''

    def __init__(self, filename, regions):
        self.original = Image.open(filename)
        self.regions = {name: self.original.crop(coords)
                        for name, coords in regions.iteritems()}
