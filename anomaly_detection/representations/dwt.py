import pywt
import numpy


def get_dwt_converter(wavelet_family='db1', **kwargs):
    """
    Returns a function that converts sequences to their wavelet representations.
    """
    return lambda sequence: numpy.concatenate(pywt.dwt(sequence, wavelet_family))
