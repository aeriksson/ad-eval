from __future__ import division
import numpy


class MeanAggregator(object):
    def __init__(self, series_length=0):
        self._mean = numpy.zeros(series_length)
        self._counts = numpy.zeros(series_length)

    def init(self, series_length):
        self._mean = numpy.zeros(series_length)
        self._counts = numpy.zeros(series_length)

    def add_score(self, score, start, end):
        for i in range(start, end + 1):
            n = self._counts[i]
            self._mean[i] = (self._mean[i] * n + score) / (n + 1)

            self._counts[i] += 1

    def get_aggregated_scores(self):
        return self._mean
