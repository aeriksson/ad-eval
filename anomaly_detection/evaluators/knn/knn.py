import heapq


class KNNEvaluator(object):
    '''
    k-Nearest Neighbors evaluator.

    Currently uses brute force to find the kNN distnce - this is the best
    we can do without extra information about the distance function.
    '''

    def __init__(self, distance, k=3):
        self._distance = distance
        self._k = k

    def evaluate(self, evaluation_series, reference_set, *args):

        distances = [self._distance(evaluation_series, s) for s in reference_set]

        # return NaN if there are not enough elements in the reference set
        if len(distances) < self._k:
            return float('NaN')

        d = heapq.nsmallest(self._k, distances)[self._k - 1]
        return d

    def requires_symbolic_input(self):
        return self._distance.IS_DISCRETE
