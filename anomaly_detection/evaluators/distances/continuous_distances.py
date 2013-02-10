"""
Distances for continuous time series go here.

TODO: add more distances!
"""

import numpy
import mlpy


def euclidean(a, b):
    assert len(a) == len(b)
    return numpy.linalg.norm(a - b)


def dynamic_time_warp(name, a, b):
    dtw = mlpy.Dtw()
    distance = dtw.compute(a, b)
    return distance

euclidean.IS_DISCRETE = False
