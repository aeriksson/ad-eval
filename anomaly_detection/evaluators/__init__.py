import knn
import svm
import distances


def get_evaluator(method='knn', k=3, distance_measure='euclidean', kernel="rbf", nu=0.1, gamma=0.1, **kwargs):
    distance = distances.get_distance(distance_measure, **kwargs)

    if method == 'knn':
        evaluator = knn.KNNEvaluator(distance=distance, k=int(k), **kwargs)
    elif method == 'svm':
        evaluator = svm.SVMEvaluator(**kwargs)
    else:
        raise NotImplementedError('Method %s not recognized' % method)

    return evaluator


def uses_discrete_distance(config_dict):
    return get_evaluator(**config_dict).uses_discrete_distance()
