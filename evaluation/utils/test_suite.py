from __future__ import division
from time import time

import distances
import result_tracker
from progress_counter import ProgressCounter


class TestSuite(object):
    def __init__(self, anomaly_detectors, anomaly_detector_labels, tests, test_labels, suite_label=None):
        self._anomaly_detectors = anomaly_detectors
        self._anomaly_detector_labels = anomaly_detector_labels
        self._tests = tests
        self._test_labels = test_labels
        self.results = result_tracker.ResultTracker(suite_label)

    def evaluate(self, display_progress=True):
        """
        Evaluates all tests on all anomaly detectors.
        """
        ad_count = len(self._anomaly_detectors)

        if display_progress:
            progress_counter = ProgressCounter()
            progress_counter.total_detectors = ad_count
            progress_counter.completed_detectors = 0

        for i in range(ad_count):
            anomaly_detector = self._anomaly_detectors[i]
            label = self._anomaly_detector_labels[i]

            self._evaluate_anomaly_detector(anomaly_detector, label, progress_counter)

            if display_progress:
                progress_counter.completed_detectors = i + 1

        progress_counter.print_progress()

    def _evaluate_anomaly_detector(self, anomaly_detector, anomaly_detector_label,
                                   progress_counter=None):
        """
        Evaluates all tests on the specified anomaly detector.
        """
        test_count = len(self._tests)

        if progress_counter is not None:
            progress_counter.total_tests = test_count
            progress_counter.completed_tests = 0

        for i in range(test_count):
            test = self._tests[i]
            test_label = self._test_labels[i]

            self._evaluate_test(anomaly_detector, anomaly_detector_label,
                           test, test_label, progress_counter)

            if progress_counter is not None:
                progress_counter.completed_tests = i + 1

    def _evaluate_test(self, anomaly_detector, anomaly_detector_label,
                       test, test_label, progress_counter=None):
        """
        Evaluates the specified test on the specified anomaly detector.
        """
        sequence_count = len(test[0])

        if progress_counter is not None:
            progress_counter.total_sequences = sequence_count
            progress_counter.completed_sequences = 0

        progress_callback = _get_progress_callback(progress_counter)
        
        for sequence, anomaly_vector in test:
            stats = _evaluate_sequence(anomaly_detector,
                progress_callback,
                sequence,
                anomaly_vector
            )

            self.results.add_record(anomaly_detector_label, test_label, **stats)

            if progress_counter is not None:
                progress_counter.completed_sequences += 1

    def print_report(self):
        self.results.print_results()


def _evaluate_sequence(anomaly_detector, progress_callback, sequence, reference_vector):
    """
    Evaluates a single sequence
    """
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
