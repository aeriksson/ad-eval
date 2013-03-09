import anomaly_detection
import eval_utils as utils
from matplotlib import pyplot

import defaults
"""
"""

AGGREGATORS = ['max', 'min', 'mean', 'median']
K_VALUES = range(1, 101, 1)
TEST_FILE = 'sequences/random_walk_added_noise'

heat_map_fig = pyplot.figure()
heat_map_plots = [heat_map_fig.add_subplot(4, 1, x + 1) for x in range(4)]

full_support_dists = []
equal_support_dists = []
euclidean_dists = []

anomaly_vectors = []

for aggregator, heat_map_plot in zip(AGGREGATORS, heat_map_plots):

    # set up anomaly detectors
    anomaly_detectors = []
    ad_config = defaults.DEFAULT_KNN_CONFIG
    for k_value in K_VALUES:
        ad_config['evaluator_config']['k'] = k_value
        ad_config['aggregator_config']['method'] = aggregator
        anomaly_detectors.append(anomaly_detection.create_anomaly_detector(**ad_config))

    # init test
    test = [utils.load_sequence(TEST_FILE)]
    test_suite = utils.TestSuite(anomaly_detectors, K_VALUES, [test], ['test'])

    # execute test
    test_suite.evaluate(display_progress=True)

    # get plots
    results = test_suite.results

    utils.plots.plot_normalized_anomaly_vector_heat_map(results, K_VALUES, plot=heat_map_plot)
    heat_map_plot.set_title(aggregator)
    heat_map_plot.set_ylabel('k')

    anomaly_vectors.append(results.get_filtered_key_values('anomaly_vector', lambda x: x['anomaly_detector'] == K_VALUES[0]))
    
    full_support_dists.append(results.get_anomaly_detector_averages(K_VALUES, 'full_support_distance'))
    equal_support_dists.append(results.get_anomaly_detector_averages(K_VALUES, 'equal_support_distance'))
    euclidean_dists.append(results.get_anomaly_detector_averages(K_VALUES, 'normalized_euclidean_distance'))

heat_map_fig.tight_layout()
heat_map_fig.show()

# plot errors
errors_fig = pyplot.figure()
error_plots = [errors_fig.add_subplot(3, 1, x + 1) for x in range(3)]

styles = ['k-', 'k:', 'k--', 'k.-']

map(lambda (vector, style, legend): error_plots[0].plot(vector, style, label=legend),
    zip(full_support_dists, styles, AGGREGATORS))
map(lambda (vector, style, legend): error_plots[1].plot(vector, style, label=legend),
    zip(equal_support_dists, styles, AGGREGATORS))
map(lambda (vector, style, legend): error_plots[2].plot(vector, style, label=legend),
    zip(euclidean_dists, styles, AGGREGATORS))

map(lambda x: x.set_xlabel('k'), error_plots)
map(lambda x: x.set_ylabel('error'), error_plots)
map(lambda x: x.legend(loc='upper left'), error_plots)

error_plots[0].set_title('Full support error')
error_plots[1].set_title('Equal support error')
error_plots[2].set_title('Normalized Euclidean error')

errors_fig.tight_layout()
errors_fig.show()

# plot heat maps
vec_fig = pyplot.figure()
vec_plot = vec_fig.gca()
map(lambda (vector, style, legend): vec_plot.plot(vector[0], style, label=legend),
    zip(anomaly_vectors, styles, AGGREGATORS))
vec_plot.legend(loc=1)
vec_plot.set_yticks([])
vec_fig.tight_layout()
vec_fig.show()
