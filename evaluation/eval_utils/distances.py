from __future__ import division
from scipy import spatial

_LENGTH_ERROR = 'Label and anomaly vectors have different lengths.'
_LABEL_ERROR = 'Found an element in label vector that is not 1'
_ANOMALY_ERROR = 'Found an element in anomaly vector smaller than 0.'


def equal_support(label_vector, anomaly_vector):
    '''
    Finds the largest threshold such that the number of elements
    a_i in anomaly_vector that are larger than t is equal to the
    number of non-zero elements in label_vector.
    Sets all elements in anomaly_vector that are larger than t
    to 1, and all others to 0. Computes the hamming distance
    between this vector and label_vector.

    Assumes that all elements in label_vector are 0 or 1,
    that all elements in anomaly_vector are larger than 1,
    and that label_vector and anomaly_vector have the same length.
    '''
    support_size = sum(l for l in label_vector)

    threshold = _get_equal_support_threshold(anomaly_vector, support_size)

    vec1 = [i == 1 for i in label_vector]
    vec2 = [a >= threshold for a in anomaly_vector]
    distance = spatial.distance.hamming(vec1, vec2)

    assert distance >= 0

    return distance


def _get_equal_support_threshold(anomaly_vector, support_size):
    '''
    Finds the smallest number t such that the number of elements
    in anomaly_vector that are larger than t is at least support_size.
    
    NOTE: complexity can be reduced by searching.
    '''

    unique_elements_sorted = reversed(sorted(set(anomaly_vector)))

    for t in unique_elements_sorted:
        if sum(a >= t for a in anomaly_vector) >= support_size:
            return t


def normalized_euclidean(label_vector, anomaly_vector):
    '''
    '''
    min_val = min(anomaly_vector)
    width = max(anomaly_vector) - min_val
    normalized_anomaly_vector = [(x - min_val) / width for x in anomaly_vector]

    distance = spatial.distance.euclidean(normalized_anomaly_vector, label_vector)

    return distance
    

def full_support(label_vector, anomaly_vector):
    '''
    Finds the largest threshold t such that for all i such that l_i = 1 (for
    l_i in label_vector), a_i > t (for a_i in anomaly_vector).
    Returns the number of elements in anomaly_vector that are larger than t
    divided by the number of non-zero elements in anomaly_vector, minus 1.

    Assumes that all elements in label_vector are 0 or 1,
    that all elements in anomaly_vector are larger than 1,
    and that label_vector and anomaly_vector have the same length.
    '''
    nonzero_indices = filter(lambda (i, val): val > 0, enumerate(label_vector))

    threshold = _get_full_support_threshold(anomaly_vector, nonzero_indices)

    vec1 = [i == 1 for i in label_vector]
    vec2 = [a >= threshold for a in anomaly_vector]
    distance = spatial.distance.hamming(vec1, vec2)

    assert distance >= 0

    return distance


def best_support(label_vector, anomaly_vector):
    """
    Finds the threshold that minimizes the error, and returns
    the corresponding error.
    """
    unique_elements = reversed(sorted(set(anomaly_vector)))

    min_distance = float('inf')

    for threshold in unique_elements:
        vec1 = [i == 1 for i in label_vector]
        vec2 = [a >= threshold for a in anomaly_vector]
        distance = spatial.distance.hamming(vec1, vec2)
        if distance < min_distance:
            min_distance = distance

    assert min_distance >= 0

    return min_distance


def _get_full_support_threshold(anomaly_vector, nonzero_indices):
    '''
    Finds the smallest number t such that the number of elements
    in anomaly_vector that are larger than t is at least support_size.
    
    NOTE: speed can be improved by using a better algorithm.
    '''

    unique_elements_sorted = reversed(sorted(set(anomaly_vector)))

    for t in unique_elements_sorted:
        if all(anomaly_vector[i] >= t for (i, _) in nonzero_indices):
            return t


def _verify_inputs(label_vector, anomaly_vector):
    '''
    Helper method for verifying inputs to distances.
    Checks vector length and verifies vector components.
    '''

    assert len(label_vector) == len(anomaly_vector), _LENGTH_ERROR

    for l in label_vector:
        assert type(l) == bool, _LABEL_ERROR

    for a in anomaly_vector:
        assert l >= 0, _ANOMALY_ERROR
