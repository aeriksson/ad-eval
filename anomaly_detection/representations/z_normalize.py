import numpy


def get_z_normalization_converter(*args):
    return lambda time_series: convert_to_z_normalized(time_series)


def convert_to_z_normalized(sequence):
    """
    Normalizes the input sequence to have zero empirical mean
    and unit empirical variance.
    """
    mean = numpy.mean(sequence)
    standard_deviation = numpy.std(sequence)
    if standard_deviation == 0:
        return numpy.zeros(len(sequence))
    modified_series = (sequence - mean) / standard_deviation
    return modified_series
