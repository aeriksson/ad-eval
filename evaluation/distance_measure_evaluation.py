import anomaly_detection
import eval_utils as utils
from matplotlib import pyplot

import defaults
"""
"""

#DISTANCE_MEASURES = ['euclidean', 'dtw']
#DISTANCE_NAMES = ['Euclidean', 'DTW']
DISTANCE_MEASURES = ['cdm']
DISTANCE_NAMES = ['CDM']
K_VALUES = range(1, 101, 1)
TEST_FILE = 'sequences/random_walk_added_noise'

heat_map_fig = pyplot.figure()
heat_map_plots = [heat_map_fig.add_subplot(2, 1, x + 1) for x in range(2)]

full_support_dists = []
equal_support_dists = []
euclidean_dists = []

for distance, name, heat_map_plot in zip(DISTANCE_MEASURES, DISTANCE_NAMES, heat_map_plots):

    # set up anomaly detectors
    anomaly_detectors = []
    ad_config = defaults.DEFAULT_KNN_CONFIG
    for k_value in K_VALUES:
        ad_config['evaluator_config']['k'] = k_value
        ad_config['evaluator_config']['distance_measure'] = distance
        ad_config['reference_filter_config'] = {'method': 'trivial'}
        anomaly_detectors.append(anomaly_detection.create_anomaly_detector(**ad_config))

    # init test
    test = [utils.load_sequence(TEST_FILE)]
    test_suite = utils.TestSuite(anomaly_detectors, K_VALUES, [test], ['test'])

    # execute test
    test_suite.evaluate(display_progress=True)

    # get plots
    results = test_suite.results

    utils.plots.plot_normalized_anomaly_vector_heat_map(results, K_VALUES, plot=heat_map_plot)
    heat_map_plot.set_title(name)
    heat_map_plot.set_ylabel('k')
    
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
    zip(full_support_dists, styles, DISTANCE_NAMES))
map(lambda (vector, style, legend): error_plots[1].plot(vector, style, label=legend),
    zip(equal_support_dists, styles, DISTANCE_NAMES))
map(lambda (vector, style, legend): error_plots[2].plot(vector, style, label=legend),
    zip(euclidean_dists, styles, DISTANCE_NAMES))

map(lambda x: x.set_xlabel('k'), error_plots)
map(lambda x: x.set_yticks([]), error_plots)
map(lambda x: x.set_xlim([1, 100]), error_plots)
map(lambda x: x.legend(loc='upper left'), error_plots)

error_plots[0].set_title('Full support')
error_plots[1].set_title('Equal support')
error_plots[2].set_title('Normalized Euclidean')

errors_fig.tight_layout()
errors_fig.show()
