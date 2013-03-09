import numpy
from matplotlib import pyplot, cm, rcParams
from mpl_toolkits.mplot3d import Axes3D
from itertools import cycle


def plot_normalized_anomaly_vectors_3d(results, label_list, plot=None, title=None, xlabel=None, ylabel=None):
    """
    Produces a 3D surface plot of the anomaly vectors associated with
    label_list.
    Assumes that there is only one test, which contains a single sequence.
    """
    fig, plot = _init_plot(plot, projection='3d')

    anomaly_vectors = _get_anomaly_vectors(results, label_list)

    X, Y = numpy.meshgrid(range(len(anomaly_vectors[0])), label_list)
    Z = numpy.array(anomaly_vectors)

    plot.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)

    _show_plot(fig, plot, title, xlabel, ylabel)

    return fig, plot


def plot_normalized_anomaly_vector_heat_map(results, label_list, plot=None,
                                            title=None, xlabel=None, ylabel=None):
    """
    Produces a heat map plot of the anomaly vectors associated with
    label_list.
    Assumes that there is only one test, which contains a single sequence.
    """
    anomaly_vectors = _get_anomaly_vectors(results, label_list)

    extent = (0, len(anomaly_vectors[0]), label_list[0], label_list[-1])

    fig, plot = _init_plot(plot)

    anomaly_vectors = numpy.flipud(numpy.array(anomaly_vectors))

    plot.imshow(anomaly_vectors, cmap=cm.coolwarm,
                interpolation='nearest', extent=extent, aspect='auto')

    _show_plot(fig, plot, title, xlabel, ylabel, xticks=[])

    return fig, plot


def plot_average_value_heat_map(results, label_matrix, x_values, y_values, key,
                                plot=None, xlabel=None, ylabel=None, title=None):
    """
    Produces a heat map of the average value of the given key.
    """
    label_matrix = numpy.array(label_matrix)
    z_values = []
    for label in label_matrix.flat:
        z = results.get_filtered_avg_over_key(key, lambda x: x['anomaly_detector'] == label)
        z_values.append(z)

    Z = numpy.reshape(z_values, (label_matrix.shape[0], label_matrix.shape[1])).T

    fig, plot = _init_plot(plot)

    extent = (x_values[0], x_values[-1], y_values[0], y_values[-1])
    
    plot.imshow(numpy.flipud(Z), cmap=cm.coolwarm, interpolation='nearest', extent=extent)

    _show_plot(fig, plot, title, xlabel, ylabel)

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

    plot.legend(loc='best')

    _show_plot(fig, plot, title, xlabel, ylabel, ylim=[0, max_val])

    return fig, plot


def plot_mean_error_values(results, ad_labels, xvalues, plot=None, title=None, xlabel=None, ylabel=None):

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

    best_support_errors = []
    for label in ad_labels:
        z = results.get_filtered_avg_over_key('best_support_distance',
                                              lambda x: x['anomaly_detector'] == label)
        best_support_errors.append(z)

    normalized_euclidean_errors = []
    for label in ad_labels:
        z = results.get_filtered_avg_over_key('normalized_euclidean_distance',
                                              lambda x: x['anomaly_detector'] == label)
        normalized_euclidean_errors.append(z)

    full_support_errors = _normalize_array(full_support_errors)
    equal_support_errors = _normalize_array(equal_support_errors)
    best_support_errors = _normalize_array(best_support_errors)
    normalized_euclidean_errors = _normalize_array(normalized_euclidean_errors)

    fig, plot = _init_plot(plot)

    plot.plot(xvalues, full_support_errors, 'k-', label='Full support error')
    plot.plot(xvalues, equal_support_errors, 'k:', label='Equal support error')
    plot.plot(xvalues, best_support_errors, 'k.-', label='Best support error')
    plot.plot(xvalues, normalized_euclidean_errors, 'k--', label='Normalized Euclidean error')

    plot.legend(loc=2)

    _show_plot(fig, plot, title, xlabel, ylabel, yticks=[], xlim=(xvalues[0], xvalues[-1]))

    return fig, plot


def plot_execution_times(results, ad_labels, xvalues, plot=None, title=None,
                         xlabel=None, ylabel=None):
    """
    Plots the execution times for the given labels.
    """

    fig, plot = _init_plot(plot)

    times = []
    for label in ad_labels:
        filter_function = lambda x: x['anomaly_detector'] == label
        z = results.get_filtered_sum_over_key('execution_time', filter_function)
                                              
        times.append(z)

    plot.plot(xvalues, times, 'k')

    if ylabel is None:
        ylabel = 'time (s)'

    xlim = (xvalues[0], xvalues[-1])
    ylim = (0, max(times) * 1.1)

    _show_plot(fig, plot, title, xlabel, ylabel, xlim=xlim, ylim=ylim)

    return fig, plot


def _get_anomaly_vectors(results, label_list):
    anomaly_vectors = []

    for label in label_list:
        filter_predicate = lambda x: x['anomaly_detector'] == label

        temp_vectors = results.get_filtered_key_values('anomaly_vector', filter_predicate)
        assert len(temp_vectors) == 1, 'Several anomaly vectors found for label %s' % label
        anomaly_vector = temp_vectors[0]

        anomaly_vector = _normalize_array(anomaly_vector)

        anomaly_vectors.append(anomaly_vector)
    return anomaly_vectors


def _normalize_array(a):
    m = min(a)
    w = max(a) - m
    return [(x - m) / w for x in a]


def _init_plot(plot, projection=None):
    figure = None

    if plot is None:
        figure = pyplot.figure(figsize=(8, 3))
        if projection is not None:
            plot = figure.gca(projection=projection)
        else:
            plot = figure.gca()

    return figure, plot


def _show_plot(fig, plot, title=None, xlabel=None, ylabel=None, xticks=None,
               yticks=None, xlim=None, ylim=None):

    if title is not None:
        plot.set_title(title)

    if ylabel is not None:
        plot.set_ylabel(ylabel)

    if xlabel is not None:
        plot.set_xlabel(xlabel)

    if xticks is not None:
        plot.set_xticks(xticks)

    if yticks is not None:
        plot.set_yticks(yticks)

    if xlim is not None:
        plot.set_xlim(xlim)

    if xlim is not None:
        plot.set_ylim(ylim)

    if fig is not None:
        fig.tight_layout()
        fig.show()
