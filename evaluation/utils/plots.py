import numpy
from matplotlib import pyplot, cm, rcParams
from mpl_toolkits.mplot3d import Axes3D
from itertools import cycle


def plot_normalized_anomaly_vectors_3d(results, label_list):
    """
    Produces a 3D surface plot of the anomaly vectors associated with
    label_list.
    Assumes that there is only one test, which contains a single sequence.
    """
    anomaly_vectors = []

    for label in label_list:
        filter_predicate = lambda x: x['anomaly_detector'] == label

        temp_vectors = results.get_filtered_key_values('anomaly_vector', filter_predicate)
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


def plot_normalized_anomaly_vector_heat_map(results, label_list, plot=None, title=None, xlabel=None, ylabel=None):
    """
    Produces a heat map plot of the anomaly vectors associated with
    label_list.
    Assumes that there is only one test, which contains a single sequence.
    """
    fig = None

    rcParams.update({'font.size': 10})

    if plot is None:
        fig = pyplot.figure(figsize=(8, 3))
        plot = fig.gca()

    anomaly_vectors = []

    for label in label_list:
        filter_predicate = lambda x: x['anomaly_detector'] == label

        temp_vectors = results.get_filtered_key_values('anomaly_vector', filter_predicate)
        assert len(temp_vectors) == 1, 'Several anomaly vectors found for label %s' % label
        anomaly_vector = temp_vectors[0]

        # rescale
        m = min(anomaly_vector)
        w = max(anomaly_vector) - m
        anomaly_vector = [(x - m) / w for x in anomaly_vector]

        anomaly_vectors.append(anomaly_vector)

    extent = (0, len(anomaly_vector), label_list[0], label_list[-1])
    plot.imshow(numpy.flipud(numpy.array(anomaly_vectors)), cmap=cm.coolwarm,
                interpolation='nearest', extent=extent, aspect='auto')

    if title is not None:
        plot.set_title(title)

    if ylabel is not None:
        plot.set_ylabel(ylabel)

    if xlabel is not None:
        plot.set_xlabel(xlabel)

    plot.set_xticks([])

    if fig is not None:
        fig.tight_layout()
        fig.show()
        return fig, plot


def plot_average_value_heat_map(results, label_matrix, x_values, y_values, key, xlabel=None, ylabel=None, title=None):
    """
    Produces a heat map of the average value of the given key.
    """
    label_matrix = numpy.array(label_matrix)
    z_values = []
    for label in label_matrix.flat:
        z = results.get_filtered_avg_over_key(key, lambda x: x['anomaly_detector'] == label)
        z_values.append(z)

    Z = numpy.reshape(z_values, (label_matrix.shape[0], label_matrix.shape[1])).T

    fig = pyplot.figure()
    plot = fig.gca()
    
    extent = (x_values[0], x_values[-1], y_values[0], y_values[-1])
    
    plot.imshow(numpy.flipud(Z), cmap=cm.coolwarm, interpolation='nearest', extent=extent)

    if xlabel is not None:
        plot.set_xlabel(xlabel)

    if ylabel is not None:
        plot.set_ylabel(ylabel)

    if title is not None:
        plot.set_title(title)

    fig.show()

    return fig, plot


def plot_anomaly_vectors(results, ad_labels, ad_legend, xlabel=None, ylabel=None,
                         title=None, normalize=False, plot=None):
    """
    Gives a simple line plot of anomaly vectors.
    Optionally shows the evaluation sequence and reference anomaly vector.
    Assumes that there is only one test, which contains a single sequence.
    """
    fig = None

    if plot is None:
        fig = pyplot.figure()
        plot = fig.gca()
    styles = cycle(['k', 'k:', 'k--', 'k-.'])

    max_val = 0

    for ad_label, legend in zip(ad_labels, ad_legend):
        filter_predicate = lambda x: x['anomaly_detector'] == ad_label

        anomaly_vector = results.get_filtered_key_values('anomaly_vector', filter_predicate)[0]

        if normalize:
            anomaly_vector = _normalize_array(anomaly_vector)

        if max(anomaly_vector) > max_val:
            max_val = max(anomaly_vector)

        plot.plot(anomaly_vector, next(styles), label=str(legend))

    if xlabel is not None:
        plot.set_xlabel(xlabel)

    if ylabel is not None:
        plot.set_ylabel(ylabel)

    if title is not None:
        plot.set_title(title)

    plot.set_ylim([0, max_val])

    plot.legend(loc='best')

    if fig is not None:
        fig.tight_layout()
        fig.show()

        return fig, plot


def plot_mean_error_values(results, ad_labels, xvalues, plot=None, title=None, xlabel=None, ylabel=None):
    fig = None

    if plot is None:
        fig = pyplot.figure()
        plot = fig.gca()

    full_support_errors = []
    for label in ad_labels:
        z = results.get_filtered_avg_over_key('full_support_distance',
                                              lambda x: x['anomaly_detector'] == label)
        full_support_errors.append(z)

    equal_support_errors = []
    for label in ad_labels:
        z = results.get_filtered_avg_over_key('equal_support_distance',
                                              lambda x: x['anomaly_detector'] == label)
        equal_support_errors.append(z)

    normalized_euclidean_errors = []
    for label in ad_labels:
        z = results.get_filtered_avg_over_key('normalized_euclidean_distance',
                                              lambda x: x['anomaly_detector'] == label)
        normalized_euclidean_errors.append(z)

    full_support_errors = _normalize_array(full_support_errors)
    equal_support_errors = _normalize_array(equal_support_errors)
    normalized_euclidean_errors = _normalize_array(normalized_euclidean_errors)

    plot.plot(xvalues, full_support_errors, 'k-', label='Full support error')
    plot.plot(xvalues, equal_support_errors, 'k:', label='Equal support error')
    plot.plot(xvalues, normalized_euclidean_errors, 'k--', label='Normalized Euclidean error')

    if title is not None:
        plot.set_title(title)

    if ylabel is not None:
        plot.set_ylabel(ylabel)

    if xlabel is not None:
        plot.set_xlabel(xlabel)

    plot.set_yticks([])
    plot.set_xlim((xvalues[0], xvalues[-1]))

    plot.legend(loc=2)

    if fig is not None:
        fig.tight_layout()
        fig.show()

        return fig, plot


def plot_execution_times(results, ad_labels, xvalues, plot=None, title=None, xlabel=None, ylabel=None):
    fig = None

    if plot is None:
        fig = pyplot.figure()
        plot = fig.gca()

    times = []
    for label in ad_labels:
        z = results.get_filtered_sum_over_key('execution_time', lambda x: x['anomaly_detector'] == label)
        times.append(z)

    plot.plot(xvalues, times, 'k')

    plot.set_xlim((xvalues[0], xvalues[-1]))
    plot.set_ylim((0, max(times) * 1.1))

    if title is not None:
        plot.set_title(title)

    if ylabel is not None:
        plot.set_ylabel(ylabel)
    else:
        plot.set_ylabel('time (s)')

    if xlabel is not None:
        plot.set_xlabel(xlabel)

    if fig is not None:
        fig.tight_layout()
        fig.show()

        return fig, plot


def _normalize_array(a):
    m = min(a)
    w = max(a) - m
    return [(x - m) / w for x in a]
