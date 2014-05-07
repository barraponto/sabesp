import re
from csv import DictWriter, DictReader
from glob import iglob
from PIL import Image, ImageFilter
from unidecode import unidecode
from cropandread import CropperReader


class SabespCR(CropperReader):
    regions = {
        'Jaguari-QNat': (356, 31, 476, 48),
        'Jaguari-Qjus': (16, 63, 136, 80),
        'Jaguari-Vop': (215, 65, 315, 82),
        'Cachoeira-QNat': (400, 168, 520, 185),
        'Cachoeira-Qjus': (118, 281, 238, 298),
        'Cachoeira-Vop': (311, 278, 411, 295),
        'Atibainha-QNat': (404, 312, 524, 329),
        'Atibainha-Qjus': (128, 383, 248, 400),
        'Atibainha-Vop': (324, 400, 424, 417),
        'PaivaCastro-QNat': (398, 478, 518, 495),
        'PaivaCastro-Qjus': (48, 498, 168, 515),
        'PaivaCastro-Vop': (258, 528, 358, 545),
        'QT5': (283, 448, 403, 465),
        'QT6': (170, 345, 290, 362),
        'QT7': (313, 193, 433, 210),
        'ESI': (398, 548, 518, 565),
    }


def sabesp_imgopt(image, rerun=0):
    radius = 14 + 2*rerun
    return image.resize(
        [n*10 for n in image.size], Image.ANTIALIAS
    ).filter(
        ImageFilter.UnsharpMask(radius=radius)
    ).convert(
        'P', palette=Image.ADAPTIVE, colors=2
    )


def sabesp_datopt(data, rerun=0):
    if rerun > 3:
        return 'ERROR'
    data = unidecode(data).replace(' ', '')
    data = data.replace(',', '.').replace('-', '.').replace('?', '7')
    search = re.compile(r'\d+\.\d+').findall(data)
    if search:
        try:
            return float(search.pop())
        except ValueError:
            return False
    else:
        return False


def sabesp_threshold(data):
    return data if isinstance(data, bool) else True


with open('data.csv', 'a+') as f:
    keys = ['date'] + SabespCR.regions.keys()
    data = [line for line in DictReader(f, keys, delimiter=',')]
    writer = DictWriter(f, keys)

    if sum(1 for i in data) == 0:
        writer.writeheader()

    for filepath in iglob('source/*.jpg'):
        if filepath[7:-4] not in [line['date'] for line in data]:
            print 'Processing {f}.'.format(f=filepath)
            try:
                writer.writerow(dict(SabespCR(filepath).read_image(
                    sabesp_imgopt, sabesp_datopt, sabesp_threshold).values,
                    date=filepath[7:-4]))
                print 'Finished processing {f}.'.format(f=filepath)
            except IOError:
                print 'Skipped {f} due to file errors.'.format(f=filepath)
        else:
            print 'Skipped {f}.'.format(f=filepath)
