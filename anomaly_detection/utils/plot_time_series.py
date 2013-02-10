import matplotlib.pyplot as plt

_MAX_PLOTS = 10
_MAX_PLOTS_EXCEEDED_ERROR = 'Maximum number of plots (%s) exceeded:'


def plot_time_series(time_series_vec, titles=None):
    '''
    Convenience function for plotting time series.
    If multiple series are passed in they are rendered
    as stacked subplots.
    '''

    num_plots = len(time_series_vec)
    num_titles = len(titles)

    fig = plt.figure()

    for i in range(num_plots):
        assert i < _MAX_PLOTS, _MAX_PLOTS_EXCEEDED_ERROR % i

        time_series = time_series_vec[i]
        title = titles[i] if i < num_titles else None

        plot = fig.add_subplot(num_plots, 1, i + 1)
        _plot_series(plot, time_series, title)

    fig.show()


def _plot_series(plot, time_series, label):
    plot.plot(time_series)
    plot.set_title(label)
    plot.set_xlabel('t')
    plot.set_xlim(0, len(time_series) - 1)
