import knn
import svm
import distances


def get_evaluator(method='knn', k=3, distance_measure='euclidean',
                  kernel="rbf", nu=0.1, gamma=0.1, **kwargs):
    """
    Returns an evaluator object with the given parameters.
    See the individual evluators for configuration.
    """
    distance = distances.get_distance(distance_measure, **kwargs)

    if method == 'knn':
        evaluator = knn.KNNEvaluator(distance=distance, k=int(k), **kwargs)
    elif method == 'svm':
        evaluator = svm.SVMEvaluator(**kwargs)
    else:
        raise NotImplementedError('Method %s not recognized' % method)

    return evaluator


def requires_symbolic_input(config_dict):
    """
    Indicates whether or not the evaluator specified by the given configuration
    requires a symbolic input format.
    """
    return get_evaluator(**config_dict).requires_symbolic_input()
