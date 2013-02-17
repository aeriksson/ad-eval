import numpy


class MinAggregator(object):
    def __init__(self, series_length=0):
        self._values = numpy.ones(series_length) * numpy.inf

    def init(self, series_length):
        self._values = numpy.ones(series_length) * numpy.inf

    def add_score(self, score, start, end):
        for i in range(start, end + 1):
            if self._values[i] > score:
                self._values[i] = score

    def get_aggregated_scores(self):
        return self._values
