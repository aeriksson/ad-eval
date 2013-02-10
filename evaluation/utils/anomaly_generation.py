"""
Various methods for building time series anomalies.
"""

import numpy
import math
import random


def flatten(sequence, interval=None):
    """
    Returns a sequence with data[i] held constant for i in the given interval.
    """
    constant = sequence[interval[0]]
    make_const = lambda _: constant
    return _map_to_interval_const(sequence, interval, make_const)


def linearize(sequence, interval=None):
    """
    Makes points between start_time and end_time linearly
    interpolate the first and last values in the interval.
    """
    start_time = interval[0]
    end_time = interval[1]
    start_point = sequence[start_time]
    end_point = sequence[end_time]
    slope = (end_point - start_point) / (end_time - start_time)
    intercept = start_point - slope * start_time

    make_linear = lambda _, t: slope * t + intercept
    return _map_to_interval_const(sequence, interval, make_linear)


def add_noise(sequence, amplitude, interval=None, random_number_generator=None):
    """
    Adds Gaussian noise of the given standard deviation and mean
    to all data in the given interval.
    """
    if random_number_generator is None:
        random_number_generator = random.Random()

    make_noise = lambda x: x + amplitude * random_number_generator.gauss(0, 1)
    return _map_to_interval_const(sequence, interval, make_noise)


def absolute_value(sequence, interval=None):
    """
    Replaces all data in the given interval with its absolute value.
    """
    return _map_to_interval_const(sequence, interval, abs)


def add_constant(sequence, constant, interval=None):
    """
    Adds a constant to all data in the given interval.
    """
    add = lambda x: constant + x
    return _map_to_interval_const(sequence, interval, add)


def multiply_constant(sequence, constant, interval=None):
    """
    Multiplies all data in the given interval by a constant.
    """
    multiply = lambda x: constant * x
    return _map_to_interval_const(sequence, interval, multiply)


def add_sine(sequence, amplitude, period, interval=None):
    """
    Adds a sine curve with the given period and amplitude
    to data in [start_time, end_time].
    """
    angular_velocity = 2 * math.pi / period
    sine = lambda x, t: x + amplitude * math.sin(angular_velocity * t)
    return _map_to_interval_dynamic(sequence, interval, sine)


def _map_to_interval_const(sequence, interval, function):
    """
    Maps a function modifying values without regard to time to the
    elements of the given time series in the given interval.
    """
    const_wrapper = lambda x, t: function(x)
    return _map_to_interval_dynamic(sequence, interval, const_wrapper)


def _map_to_interval_dynamic(sequence, interval, function):
    """
    Maps a function modifying values with regard to time to the
    elements of the given time series in the given interval.
    """
    if interval is None:
        interval = [0, len(sequence)]
    _verify_interval(sequence, interval)

    interval_wrapper = lambda x, t: function(x, t) if t in range(interval[0], interval[1]) else x
    return numpy.vectorize(interval_wrapper)(sequence, range(len(sequence)))


def _verify_interval(sequence, interval):
    assert 0 <= interval[0] <= interval[1] < len(sequence)
