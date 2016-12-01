import os

from sic import imageprocessing as impr


IMAGE_FILE = 'mandelbrot.jpg'
IMAGE_PATH = os.path.join(os.path.dirname(__file__), IMAGE_FILE)

WIDTH, HEIGHT, IMG_DATA = impr.load_image(IMAGE_PATH)


def rgb_intensity(r, g, b):
    return (r + r + r + b + g + g + g + g) >> 3


def delta_intensities(intensities):
    return [b - a for a, b in zip(intensities, intensities[1:])]


def stretch_data(times_x, data):
    return [d for d in data for _ in range(times_x)]


def coords_between(p0, p1, n_steps):
    x0, y0 = p0
    x1, y1 = p1
    dx = 1.0 * (x1 - x0) / n_steps
    dy = (1.0 * y1 - y0) / n_steps

    return [(x0 + dx * n, y0 + dy * n) for n in range(n_steps + 1)]


def get_idx(x, y):
    return y * WIDTH + x


def get_rgbs(many_coords):
    return [IMG_DATA[get_idx(int(x), int(y))] for x, y in many_coords]
