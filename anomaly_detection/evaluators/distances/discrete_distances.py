"""
Distances for discrete time series go here.

TODO: add more
"""

import zlib
import bz2

_CDM_INPUT_ERROR = 'Distance input type must be str. Got %s and %s'


def cdm(a, b, a_complexity=None, b_complexity=None):
    """
    Estimates the Compressive-based Dissimilarity Measure of two strings
    """

    ta = type(a)
    tb = type(b)
    assert ta == tb == str, _CDM_INPUT_ERROR % (ta, tb)

    if a_complexity is None:
        a_complexity = _estimate_kolmogorov_complexity(a)
    if b_complexity is None:
        b_complexity = _estimate_kolmogorov_complexity(b)

    ab_complexity = _estimate_kolmogorov_complexity(a.join(b))

    estimated_cdm = ab_complexity / float(a_complexity + b_complexity)

    return estimated_cdm


def _estimate_kolmogorov_complexity(s):
    """
    Estimates the Kolmogorov complexity of the string s by employing
    various compression algorithms and taking the minimum size.
    """
    return min(len(zlib.compress(str(s), 9)), len(bz2.compress(str(s))))

cdm.IS_DISCRETE = True
