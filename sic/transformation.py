import numpy as np
from sklearn.base import TransformerMixin
from sklearn import preprocessing
import pylab


class CircularBuffer(object):

    def __init__(self, size):
        self._size = size
        self._index = 0
        self._n_populated = 0
        self._data = [0] * size

    def push_back(self, value):
        self._data[self._index] = value
        self._index += 1
        if self._index == self._size:
            self._index = 0
        if self._n_populated < self._size:
            self._n_populated += 1

    def front(self):
        index = self._index if self._n_populated >= self._size else 0
        return self._data[index]

    def n_populated(self):
        return self._n_populated

    def mean(self):
        return np.mean(self._data[:self._n_populated])


class IIRFilter(object):

    def __init__(self, window):
        self._filtered = 0
        self._window = window
        self._inverse_window = 1. / window
        self._data = CircularBuffer(window)

    def next(self, unfiltered):
        self._data.push_back(unfiltered)
        if self._data.n_populated() < self._window:
            self._filtered = self._data.mean()
        else:
            self._filtered += self._inverse_window * (unfiltered - self._data.front())
        return self._filtered


class Play(TransformerMixin):

    def transform(self, X, *_):
        array = []
        for tup in X:
            array.append(tup[0] + tup[1] + tup[2])
        res = np.asarray(array)
#        pylab.plot(range(len(res)), res, 'r')
        return res

    def fit(self, *_):
        return self


class Smoother(TransformerMixin):

    def transform(self, X, *_):
        filt = IIRFilter(6)
        res = []
        for x in X:
            res.append(filt.next(x))
#        pylab.plot(range(len(res)), res)
        return np.asarray(res)

    def fit(self, *_):
        return self


class InverseFFT(TransformerMixin):

    def transform(self, X, *_):
        array = []
        for tup in X:
            array.append(np.complex(np.log(tup[0]), np.log(tup[1])))
        return np.abs(np.fft.ifft(array))

    def fit(self, *_):
        return self


class Normalizer(TransformerMixin):

    def transform(self, X, *_):
        return preprocessing.MinMaxScaler((-1, 1)).fit_transform(X.reshape(-1, 1))[:, 0]

    def fit(self, *_):
        return self
