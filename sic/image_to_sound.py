from sic import argparsing, imageprocessing
from sic.transformation import InverseFFT, Normalizer
from sklearn.pipeline import Pipeline
from sic.audio_file import play_audio_block


def main():
    args = argparsing.parse_args()
    width, height, image_data = imageprocessing.load_image(args.image)
    X = imageprocessing.pixel_sampler(width, height, image_data)
    pipeline = Pipeline(
        [("inverse_fft", InverseFFT()),
         ("normalizer", Normalizer())],
    )
    data = pipeline.fit_transform(X)
    play_audio_block(data)
