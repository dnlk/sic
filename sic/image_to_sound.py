from sic import argparsing
from sic.transformation import InverseFFT, Normalizer
from sklearn.pipeline import Pipeline

import imageprocessing

def main():
    args = argparsing.parse_args()

    image_data = imageprocessing.load_image( args.image )

    print image_data

    pipeline = Pipeline(
        [("inverse_fft", InverseFFT()),
         ("normalizer" , Normalizer())],
    )
#    data = pipeline.transform(X)