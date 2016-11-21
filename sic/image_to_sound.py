from sic import argparsing
from sic.transformation import InverseFFT, Normalizer
from sklearn.pipeline import Pipeline


def main():
    args = argparsing.parse_args()
    print vars(args)
    pipeline = Pipeline(
        [("inverse_fft", InverseFFT()),
         ("normalizer" , Normalizer())],
    )
#    data = pipeline.transform(X)
