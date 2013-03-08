import numpy

_DIMENSION_ERROR = ('Target dimension ({target_dimension}) must be smaller '
                    'than original dimension ({original_dimension}).')


def convert_to_paa(sequence, target_dimension=10):
    """
    Generates a PAA (Piecewise Aggregate Approximation)
    representation of the given time series.
    """
    original_dimension = len(sequence)
    if target_dimension == original_dimension:
        return sequence.copy()
    
    assert target_dimension < original_dimension, _DIMENSION_ERROR.format(
        target_dimension=target_dimension,
        original_dimension=original_dimension
    )

    sample_width = original_dimension / target_dimension

    new_series = numpy.zeros(target_dimension)

    j = 0
    for i in range(original_dimension):
        pt = time_series[i]

        next_step = sample_width * (j + 1)
        d1 = next_step - i
        d2 = (i + 1) - next_step

        new_series[j] += pt * min(1, d1)

        if d2 >= 0 and i < original_dimension - 1:
            new_series[j + 1] += pt * d2
            j += 1

    return new_series
