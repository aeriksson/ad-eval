from __future__ import division

import numpy
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D


class ResultTracker(object):
    """
    Class for keeping track of and displaying test results.
    Currently suffers from horrible complexity.
    However, this is not likely to be a problem except for huge tests.
    """

    def __init__(self, suite_label):
        self._suite_label = suite_label
        self._results = []
        self._anomaly_detector_labels = set()
        self._test_labels = set()

    def add_record(self, anomaly_detector_label, test_label, execution_time=None,
                   equal_support_distance=None, full_support_distance=None,
                   normalized_euclidean_distance=None, anomaly_vector=None):

        self._anomaly_detector_labels.add(anomaly_detector_label)
        self._test_labels.add(test_label)

        self._results.append({
            'anomaly_detector': anomaly_detector_label,
            'test': test_label,
            'execution_time': execution_time,
            'equal_support_distance': equal_support_distance,
            'full_support_distance': full_support_distance,
            'normalized_euclidean_distance': normalized_euclidean_distance,
            'anomaly_vector': anomaly_vector
        })

    def update(self, other_results):
        """
        Updates the results object by adding all elements in other_results to it.
        """

        self._anomaly_detector_labels.update(other._anomaly_detector_labels)
        self._test_labels.update(other._test_labels)
        self._results._extend(other._results)

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

        relevance_filter = (lambda x: x['anomaly_detector'] == ad_label and x['test'] == test_label)

        self._print_test_details(relevance_filter)

    def _print_anomaly_detection_totals(self, ad_label):
        print("\n\t\tTotal:")

        relevance_filter = (lambda x: x['anomaly_detector'] == ad_label)

        self._print_test_details(relevance_filter)

    def _print_test_details(self, relevance_filter):
        total_execution_time = self.get_filtered_sum_over_key('execution_time', relevance_filter)
        avg_equal_support = self.get_filtered_avg_over_key('equal_support_distance', relevance_filter)
        avg_full_support = self.get_filtered_avg_over_key('full_support_distance', relevance_filter)
        avg_euclidean = self.get_filtered_avg_over_key('normalized_euclidean_distance', relevance_filter)

        if total_execution_time is not None:
            print("\t\t\tTotal execution time (s):              %.2f" % total_execution_time)
        if avg_equal_support is not None:
            print("\t\t\tAverage equal support distance:        %.3f" % avg_equal_support)
        if avg_full_support is not None:
            print("\t\t\tAverage full support distance:         %.3f" % avg_full_support)
        if avg_euclidean is not None:
            print("\t\t\tAverage normalized Euclidean distance: %.3f" % avg_euclidean)

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

    def get_normalized_anomaly_vector_plot(self, label_list):
        """
        Produces a 3D surface plot of the anomaly vectors associated with
        label_list.
        """
        anomaly_vectors = []

        for label in label_list:
            filter_predicate = lambda x: x['anomaly_detector'] == label

            temp_vectors = self.get_filtered_key_values('anomaly_vector', filter_predicate)
            assert len(temp_vectors) == 1, 'Several anomaly vectors found for label %s' % label
            anomaly_vector = temp_vectors[0]

            # rescale
            m = min(anomaly_vector)
            w = max(anomaly_vector) - m
            anomaly_vector = [(x - m) / w for x in anomaly_vector]

            anomaly_vectors.append(anomaly_vector)

        X, Y = numpy.meshgrid(range(len(anomaly_vectors[0])), label_list)
        Z = numpy.array(anomaly_vectors)

        fig = pyplot.figure()
        plot = fig.gca(projection='3d')
        plot.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
        return fig, plot

    def get_average_value_plot(self, label_matrix, x_values, y_values, key):
        """
        Produces a 3D plot of the average value of the given key.
        """
        label_matrix = numpy.array(label_matrix)
        z_values = []
        for label in label_matrix.flat:
            z = self.get_filtered_avg_over_key(key, lambda x: x['anomaly_detector'] == label)
            z_values.append(z)

        X, Y = numpy.meshgrid(x_values, y_values)
        Z = numpy.reshape(z_values, label_matrix.shape)

        fig = pyplot.figure()
        plot = fig.gca(projection='3d')
        plot.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)
        return fig, plot
