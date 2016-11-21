import numpy as np
from sklearn.base import TransformerMixin
from sklearn import preprocessing


class InverseFFT(TransformerMixin):

    def transform(self, X, *_):
        array = []
        for tup in X:
            array.append(np.complex(tup[0], tup[1]))
        return np.abs(np.fft.ifft(array))

    def fit(self, *_):
        return self


class Normalizer(TransformerMixin):

    def transform(self, X, *_):
        return preprocessing.MinMaxScaler((-1, 1)).fit_transform(X.reshape(-1, 1))[:, 0]

    def fit(self, *_):
        return self
