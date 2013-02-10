import numpy


class MedianAggregator(object):
    def __init__(self, series_length=0):
        self._values = []

    def init(self, series_length):
        self._values = []
        for _ in range(series_length):
            self._values.append([])

    def add_score(self, score, start, end):
        for i in range(start, end + 1):
            self._values[i].append(score)

    def get_aggregated_scores(self):
        return [numpy.median(x) for x in self._values]
