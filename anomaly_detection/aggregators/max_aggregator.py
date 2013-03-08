import numpy


class MaxAggregator(object):
    """
    Constructs an anomaly vector with the maximum anomaly score
    for each item.
    """
    def __init__(self, series_length=0):
        self._values = numpy.zeros(series_length)

    def init(self, series_length):
        self._values = numpy.zeros(series_length)

    def add_score(self, score, start, end):
        for i in range(start, end + 1):
            if self._values[i] < score:
                self._values[i] = score

    def get_aggregated_scores(self):
        return self._values
