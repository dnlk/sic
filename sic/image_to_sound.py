from sic import argparsing, imageprocessing
from sic.transformation import InverseFFT, Normalizer, Play, Smoother
from sklearn.pipeline import Pipeline
from sic.audio_file import play_audio_block
from sic.imageprocessing import SamplingOptions
import pylab


def main():
    args = argparsing.parse_args()
    width, height, image_data = imageprocessing.load_image(args.image)
    X = imageprocessing.pixel_sampler(width, height, image_data, SamplingOptions.REDGREEN)
    pipeline = Pipeline([
        ("play", Play()),
#        ("InverseFFT", InverseFFT()),
#        ("normalizer1", Normalizer()),
#        ("smoother", Smoother()),
        ("normalizer2", Normalizer()),
    ])
    data = pipeline.fit_transform(X)
#    pylab.show()
    play_audio_block(data)
