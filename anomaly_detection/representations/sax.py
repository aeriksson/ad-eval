import numpy
from scipy.stats import norm

from paa import convert_to_paa
from z_normalize import convert_to_z_normalized


def get_sax_converter(dimensions, alphabet_size, **kwargs):
    return lambda time_series: convert_to_sax(time_series, dimensions, alphabet_size)


def convert_to_sax(time_series, sample_count, alphabet_size):
    """
    Returns the SAX representation (with with the specified sample count
    and alphabet size) of the given time series, with the alphabet given as
    the n first integers.

    TODO: return a binary array instead of a string?
    """
    paa_representation = convert_to_paa(time_series, sample_count)
    normalized_series = convert_to_z_normalized(paa_representation)
    equipartition = _get_normal_cdf_equipartition(alphabet_size)
    sax_representation = _symbolize_series(normalized_series, equipartition)
    string_representation = _convert_to_string(sax_representation)
    return string_representation


def _symbolize_series(time_series, equipartition):
    """
    Given a set of frames (assumed to be Z-normalized), converts them to
    the symbolic representation given by the equipartition.
    """
    ret = numpy.zeros(len(equipartition))
    for i in range(len(time_series)):
        ret[i] = _convert_to_symbol(time_series[i], equipartition)
    return ret


def _convert_to_symbol(datapoint, equipartition):
    """
    Returns the index of the symbol given by the data point.
    The data point should be drawn from a normalized N(0,1) distribution.
    """
    # TODO: it's possible to optimize this
    if datapoint < equipartition[0]:
        return 0
    if datapoint > equipartition[-1]:
        return len(equipartition)

    for i in range(len(equipartition) - 1):
        if equipartition[i] < datapoint and datapoint < equipartition[i + 1]:
            return i
    raise Exception("Data point %s not in equipartition %s" % (datapoint, equipartition))


def _get_normal_cdf_equipartition(n):
    """
    Returns a set {x_i} of (n - 1) numbers such that:
      * P(N(0,1) < x_0) = a
      * P(x_{i} < N(0,1) < x_{i+1}) = a
      * P(N(0,1) > x_{n-2}) = a
    where a = 1 / n.
    Requires n > 1
    """
    assert n > 1
    return [norm.ppf(x) for x in numpy.linspace(0, 1, n)]


def _convert_to_string(arr):
    return ''.join([chr(int(i) + ord('a')) for i in arr])
