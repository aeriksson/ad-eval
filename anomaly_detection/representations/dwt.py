import pywt
import numpy


def get_dwt_converter(**kwargs):
    return lambda sequence: numpy.concatenate(pywt.dwt(sequence, 'db1'))
