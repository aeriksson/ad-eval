import numpy
import random

import anomaly_generation
import performance_test

_LENGTH_ERROR = "Invalid subsequence length: %s"


def generate_specified_single_sequence_test(base_sequence, anomaly_type, amplitude, interval,
                                            random_number_generator=None):
    """Convenience method for generating a test containing a single sequence.
    
    Wraps the arguments and passes them to generate_specified_test. See that
    function for more details.
    """
    return generate_specified_test([base_sequence], [anomaly_type], [amplitude], [interval],
                                   random_number_generator)


def generate_specified_test(base_sequences, anomaly_types, amplitudes, intervals,
                            random_number_generator=None):
    """Generates a performance test from lists of parameters.

    The i:th element of all arguments are used to generate the i:th sequence
    in the performance test. This means that all arguments must have the same
    length.

    This function is limited in the types of tests it can create. Specifically,
    it can only create one (artificial) anomaly per sequence. For more control,
    use RandomAnomalyGenerator or create the sequences manually.

    Args:
        base_sequences: A list of sequences to use as bases when adding anomalies.
        anomaly_types: A list of the names of the anomaly types to use.
        amplitudes: A list of amplitudes for the anomalies.
        intervals: A list of start and end positions (inclusive) for the anomalies.

    Returns:
        A list of tuples containing the test.
    """
    specifications = zip(base_sequences, anomaly_types, amplitudes, intervals)
    sequences = []
    anomaly_vectors = []

    for (base_sequence, anomaly_type, amplitude, interval) in specifications:

        length = len(base_sequence)
        anomaly_function = _get_anomaly_function_from_type(anomaly_type,
                                random_number_generator=random_number_generator)

        anomaly_vector = [1 if interval[0] <= x <= interval[1] else 0 for x in range(length)]
        sequence = anomaly_function(base_sequence, amplitude, interval)

        sequences.append((sequence, anomaly_vector))

    return sequences


def generate_random_test(base_sequence, count, anomaly_type, amplitude_interval,
                         width_interval, random_number_generator=None):
    """Randomly generates a test containing similar sequences.

    This function is limited in the types of tests it can create. Specifically,
    it can only create one (artificial) anomaly per sequence. For more control,
    use RandomAnomalyGenerator or create the sequences manually.

    Args:
        base_sequences: A list of sequences to use as bases when adding anomalies.
        anomaly_types: A list of the names of the anomaly types to use.
        amplitudes: A list of amplitudes for the anomalies.
        intervals: A list of start and end positions (inclusive) for the anomalies.
        random_number_generator: An (optional) RNG to use.

    Returns:
        A list of tuples containing the test.
    """
    anomaly_function = _get_anomaly_function_from_type(anomaly_type)
    anomaly_generator = RandomAnomalyGenerator(
        amplitude_interval, width_interval, anomaly_function, random_number_generator)

    return [anomaly_generator.add_single_anomaly(base_sequence) for _ in range(count)]


def _get_anomaly_function_from_type(anomaly_type, **kwargs):
    if anomaly_type == 'sine':
        def anomaly_function(sequence, amplitude, interval):
            return anomaly_generation.add_sine(sequence, amplitude, interval[1] - interval[0],
                                               interval, **kwargs)

        return anomaly_function

    elif anomaly_type == 'noise':
        def anomaly_function(sequence, amplitude, interval):
            return anomaly_generation.add_noise(sequence, amplitude, interval, **kwargs)

        return anomaly_function

    else:
        raise Exception('unknown anomaly type: %s' % anomaly_type)


class RandomAnomalyGenerator(object):

    def __init__(self, amplitude_interval, width_interval, anomaly_function, random_number_generator=None):
        self._amplitude_interval = amplitude_interval
        self._width_interval = width_interval
        self._anomaly_function = anomaly_function

        if random_number_generator is None:
            random_number_generator = random.Random()
        self._rng = random_number_generator

    def add_single_anomaly(self, sequence):
        amplitude = self._rng.uniform(*self._amplitude_interval)

        sequence_length = len(sequence)

        interval = self._generate_subsequence_interval(sequence_length)
        
        modified_sequence = self._anomaly_function(sequence=sequence, amplitude=amplitude, interval=interval)

        anomaly_vector_generator = self._get_anomaly_vector_generator(sequence_length, *interval)
        
        return modified_sequence, list(anomaly_vector_generator)

    def _generate_subsequence_interval(self, sequence_length):
        subsequence_length = self._rng.randint(*self._width_interval)

        assert subsequence_length > 0, _LENGTH_ERROR % subsequence_length
       
        start_pos = self._rng.randrange(0, sequence_length - subsequence_length)
        end_pos = start_pos + subsequence_length - 1

        return (start_pos, end_pos)

    def _get_anomaly_vector_generator(self, sequence_length, start, end):
        return (1 if (start <= i and i <= end) else 0 for i in range(sequence_length))

    def add_multiple_anomalies(self, sequence, number_of_anomalies):
        modified_sequence = sequence
        anomaly_vector = (0 for _ in range(len(sequence)))

        for _ in range(number_of_anomalies):
            modified_sequence, temp_anomaly_vector = self.add_single_anomaly(modified_sequence)
            anomaly_vector = (i or j for (i, j) in zip(anomaly_vector, temp_anomaly_vector))

        return modfied_sequence, anomaly_vector
