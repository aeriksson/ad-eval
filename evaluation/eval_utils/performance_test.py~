from time import time

import distances


class PerformanceTest(object):
    """
    TODO: make this object a container only and let test_suite handle the logic.
    """
    def __init__(self, test_sequences, reference_anomaly_vectors):
        self._sequences = test_sequences
        self._reference_vectors = reference_anomaly_vectors
        self._sequence_count = len(test_sequences)

    def run(self, anomaly_detector, store_results_callback, progress_counter=None):
        if progress_counter is not None:
            progress_counter.total_sequences = self._sequence_count
            progress_counter.completed_sequences = 0

        progress_callback = _get_progress_callback(progress_counter)
        
        for i in range(self._sequence_count):

            stats = _evaluate_sequence(anomaly_detector,
                progress_callback,
                self._sequences[i],
                self._reference_vectors[i]
            )

            store_results_callback(**stats)

            if progress_counter is not None:
                progress_counter.completed_sequences = i + 1


def _evaluate_sequence(anomaly_detector, progress_callback, sequence, reference_vector):
    start_time = time()

    anomaly_vector = anomaly_detector.evaluate(sequence, progress_callback)

    execution_time = time() - start_time

    return {
        'execution_time': execution_time,
        'equal_support_distance': distances.equal_support(reference_vector, anomaly_vector),
        'full_support_distance': distances.full_support(reference_vector, anomaly_vector),
        'normalized_euclidean_distance': distances.normalized_euclidean(reference_vector, anomaly_vector),
        'anomaly_vector': anomaly_vector
    }


def _get_progress_callback(progress_counter):
    def callback(progress_fraction):
        progress_counter.sequence_progress = progress_fraction
        progress_counter.print_progress()

    return callback
