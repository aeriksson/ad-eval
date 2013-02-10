'''
This module contains methods for aggregating several overlapping
time series.
'''
import max_aggregator
import mean_aggregator
import median_aggregator


def get_aggregator(method='max'):
    return {
        'max': max_aggregator.MaxAggregator(),
        'mean': mean_aggregator.MeanAggregator(),
        'median': median_aggregator.MedianAggregator()
    }[method]
