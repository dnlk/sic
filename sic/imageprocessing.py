from PIL import Image


def load_image(filename):
    im = Image.open(filename)
    pixels = list(im.getdata())
    width, height = im.size
    return width, height, pixels


class SamplingOptions:
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    GREYSCALE = 'greyscale'
    REDGREEN = 'redgreen'


def pixel_sampler(width, height, data, sample_option=SamplingOptions.GREYSCALE):
    result = []

    for x in data:
        if sample_option == 'red':
            pixel = (x[0] + 1, x[0] + 1)
        elif sample_option == 'green':
            pixel = (x[1] + 1, x[1] + 1)
        elif sample_option == 'redgreen':
            pixel = (x[0] + 1, x[1] + 1, x[2] + 1)
        elif sample_option == 'blue':
            pixel = (x[2] + 1, x[2] + 1)
        elif sample_option == 'greyscale':
            greyscale = 0.2126 * (x[0] + 1) + 0.7152 * (x[1] + 1) + 0.0722 * (x[2] + 1)
            pixel = (greyscale, greyscale)
        result.append(pixel)
    return result
