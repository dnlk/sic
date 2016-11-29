import numpy as np

from sic import imageprocessing as impr
from sic import harmonic_oscillator
from sic import audio_file

IMAGE_PATH = 'C:/Users/Dan/Desktop/Projects/hackathon/sic/sic/mandelbrot.jpg'
HEIGHT = 1080
WIDTH = 1920


def rgb_intensity(r, g, b):
    return (r + r + r + b + g + g + g + g) >> 3


def stretch_data(times_x, data):
    return [d for d in data for _ in range(times_x)]


if __name__ == '__main__':

    img_data = impr.load_image(IMAGE_PATH)
    slice_down_the_middle = img_data[2][WIDTH // 2::WIDTH]
    intensities = [rgb_intensity(*rgb) for rgb in slice_down_the_middle]
    delta_intensities = [b - a for a, b in zip(intensities, intensities[1:])]
    stretched = stretch_data(45, delta_intensities)

    if __name__ == '__main__':

        osc = harmonic_oscillator.Oscillator(
            mass=.0001,
            position=0,
            velocity=0,
            acceleration=0,
            friction_coef=0,
            spring_coef=10000,
        )

        DT = 1.0 / 44100
        SECONDS_AUDIO = 1
        SAMPLE_RATE = 44100
        NUM_SAMPLES = SAMPLE_RATE * SECONDS_AUDIO

        EXT_F = stretched

        array = np.zeros((NUM_SAMPLES, 1))

        for i in range(NUM_SAMPLES):
            osc.update(EXT_F[i] * 5000, DT)
            # osc.update(0, DT)

            array[i] = osc.position

        print(array)
        audio_file.play_audio_block(array)
