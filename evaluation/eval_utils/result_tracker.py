from __future__ import division

import numpy


class ResultTracker(object):
    """
    Keeps track of and displays test results.

    Supports limited aggregation and filtering of results.

    Note that while the aggregation is inefficient, this is not likely
    to be a problem except for huge tests.
    """

    def __init__(self, suite_label):
        self._suite_label = suite_label
        self._results = []
        self._anomaly_detector_labels = set()
        self._test_labels = set()

    def add_record(self, anomaly_detector_label, test_label, execution_time=None,
                   equal_support_distance=None, full_support_distance=None,
                   best_support_distance=None, normalized_euclidean_distance=None,
                   anomaly_vector=None):

        self._anomaly_detector_labels.add(anomaly_detector_label)
        self._test_labels.add(test_label)

        self._results.append({
            'anomaly_detector': anomaly_detector_label,
            'test': test_label,
            'execution_time': execution_time,
            'equal_support_distance': equal_support_distance,
            'full_support_distance': full_support_distance,
            'best_support_distance': best_support_distance,
            'normalized_euclidean_distance': normalized_euclidean_distance,
            'anomaly_vector': anomaly_vector
        })

    def get_filtered_key_values(self, key, filter_predicate):
        """
        Returns the values of the field specified by key,
        in all entries, filtered by filter_predicate.

        Entries that do not contain the key are ignored.
        """
        wrapped_filter = lambda x: x[key] is not None and filter_predicate(x)
        return [x[key] for x in filter(wrapped_filter, self._results)]

    def get_filtered_sum_over_key(self, key, filter_predicate):
        """
        Returns the average of the field specified by key,
        in all elements, filtered by filter_predicate.
        """
        return sum(self.get_filtered_key_values(key, filter_predicate))

    def get_filtered_avg_over_key(self, key, filter_predicate):
        """
        Returns the average of the field specified by key,
        in all elements, filtered by filter_predicate.
        """
        values = self.get_filtered_key_values(key, filter_predicate)

        if len(values) == 0:
            return None
        else:
            return sum(values) / len(values)

    def get_anomaly_detector_averages(self, ad_labels, key):
        """
        Returns a list of the average value of 'key' over the anomaly
        detector labels in ad_labels.
        """
        filter_function = lambda x: x['anomaly_detector'] == l
        return [self.get_filtered_avg_over_key(key, filter_function) for l in ad_labels]

    def print_results(self):
        self._print_header()

        for ad_label in self._anomaly_detector_labels:
            self._print_anomaly_detection_header(ad_label)

            for test_label in self._test_labels:
                self._print_test_results(ad_label, test_label)

            self._print_anomaly_detection_totals(ad_label)

    def _print_header(self):
        print("\n\nResults for test suite '%s':" % self._suite_label)

    def _print_anomaly_detection_header(self, label):
        print("\n\tAnomaly detector '%s':" % label)

    def _print_test_results(self, ad_label, test_label):
        print("\n\t\tTest '%s':" % test_label)

        relevance_filter = lambda x: x['anomaly_detector'] == ad_label and x['test'] == test_label

        self._print_test_details(relevance_filter)

    def _print_anomaly_detection_totals(self, ad_label):
        print("\n\t\tTotal:")

        relevance_filter = (lambda x: x['anomaly_detector'] == ad_label)

        self._print_test_details(relevance_filter)

    def _print_test_details(self, relevance_filter):
        total_execution_time = self.get_filtered_sum_over_key('execution_time', relevance_filter)
        avg_equal_support = self.get_filtered_avg_over_key('equal_support_distance', relevance_filter)
        avg_full_support = self.get_filtered_avg_over_key('full_support_distance', relevance_filter)
        avg_best_support = self.get_filtered_avg_over_key('best_support_distance', relevance_filter)
        avg_euclidean = self.get_filtered_avg_over_key('normalized_euclidean_distance', relevance_filter)

        if total_execution_time is not None:
            print("\t\t\tTotal execution time (s):              %.2f" % total_execution_time)
        if avg_equal_support is not None:
            print("\t\t\tAverage equal support distance:        %.3f" % avg_equal_support)
        if avg_full_support is not None:
            print("\t\t\tAverage full support distance:         %.3f" % avg_full_support)
        if avg_best_support is not None:
            print("\t\t\tAverage best support distance:         %.3f" % avg_best_support)
        if avg_euclidean is not None:
            print("\t\t\tAverage normalized Euclidean distance: %.3f" % avg_euclidean)
