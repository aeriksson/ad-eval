import anomaly_detection
import utils

import defaults

"""
Visualizes the impact of the sliding window width on anomaly detection accuracy
by evaluating the accuracy of a given (sliding window) kNN anomaly detection
problem on a single sequence.
"""

WINDOW_WIDTHS = range(1, 51, 1)
TEST_FILE = 'sequences/random_walk_added_noise'

# set up anomaly detectors
anomaly_detectors = []
ad_config = defaults.DEFAULT_KNN_CONFIG
for width in WINDOW_WIDTHS:
    filter_config = {'method': 'sliding_window', 'width': width, 'step': 1}
    ad_config['evaluation_filter_config'] = filter_config
    ad_config['reference_filter_config'] = filter_config
    anomaly_detectors.append(anomaly_detection.create_anomaly_detector(**ad_config))

# init test
test = [utils.load_sequence(TEST_FILE)]
test_suite = utils.TestSuite(anomaly_detectors, WINDOW_WIDTHS, [test], ['test'])

# execute test
test_suite.evaluate(display_progress=True)

# get plot
results = test_suite.results
fig1, plot1 = utils.plot_normalized_anomaly_vector_heat_map(results, WINDOW_WIDTHS, ylabel='w')
fig2, plot2 = utils.plot_mean_error_values(results, WINDOW_WIDTHS, WINDOW_WIDTHS, xlabel='w')
fig3, plot3 = utils.plot_execution_times(results, WINDOW_WIDTHS, WINDOW_WIDTHS, xlabel='w')
