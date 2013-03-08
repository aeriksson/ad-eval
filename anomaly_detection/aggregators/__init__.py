'''
Module contains methods for aggregating interval anomaly scores
to anomaly vectors.
'''
import max_aggregator
import mean_aggregator
import median_aggregator
import min_aggregator


def get_aggregator(method='max'):
    return {
        'max': max_aggregator.MaxAggregator(),
        'min': min_aggregator.MinAggregator(),
        'mean': mean_aggregator.MeanAggregator(),
        'median': median_aggregator.MedianAggregator()
    }[method]
