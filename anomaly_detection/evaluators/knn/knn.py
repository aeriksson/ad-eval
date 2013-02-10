'''
k-Nearest Neighbors evaluator.

Currently uses brute force to find the kNN distnce - this is the best
we can do without prior information about the distance function.

TODO: use ANN for approximate Minkowski kNN.
'''

import heapq


class KNNEvaluator(object):

    _training_series = []

    def __init__(self, distance, k=3):
        self._distance = distance
        self._k = k

    def evaluate(self, evaluation_series, reference_set, *args):
        distances = [self._distance(evaluation_series, s) for s in reference_set]
        d = heapq.nsmallest(self._k, distances)[self._k - 1]
        return d

    def uses_discrete_distance(self):
        return self._distance.IS_DISCRETE
