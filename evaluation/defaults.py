

_DEFAULT_FILTER_CONFIG = {'method': 'sliding_window', 'width': 10, 'step': 1}

DEFAULT_KNN_CONFIG = {
    'evaluation_filter_config': _DEFAULT_FILTER_CONFIG,
    'context_config': {'method': 'trivial'},
    'reference_filter_config': _DEFAULT_FILTER_CONFIG,
    'evaluator_config': {'method': 'knn', 'distance_measure': 'euclidean'},
    'aggregator_config': {'method': 'mean'},
    'discretization_config': {'method': 'sax', 'dimensions': 10, 'alphabet_size': 10}
}
