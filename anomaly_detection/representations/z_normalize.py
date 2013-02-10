import numpy


def get_z_normalization_converter(*args):
    return lambda time_series: convert_to_z_normalized(time_series)


def convert_to_z_normalized(time_series):
    """
    Assuming that the time series is drawn from a N(a,b) distribution,
    normalizes (Z-normalization) it to have been drawn from N(0,1).
    """
    mean = numpy.mean(time_series)
    standard_deviation = numpy.std(time_series)
    if standard_deviation == 0:
        return numpy.zeros(len(time_series))
    modified_series = (time_series - mean) / standard_deviation
    return modified_series
