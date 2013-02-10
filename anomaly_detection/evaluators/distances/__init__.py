import scipy

from continuous_distances import dynamic_time_warp, euclidean
from discrete_distances import cdm


def get_distance(distance_measure='euclidean', **kwargs):

    if distance_measure == 'euclidean':
        distance = euclidean
    elif distance_measure == 'dtw':
        distance = dynamic_time_warp
    elif distance_measure == 'cdm':
        distance = cdm
    else:
        raise NotImplementedError('Unknown distance')

    return distance
