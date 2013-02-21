import anomaly_detection
import utils

import defaults

"""
Visualizes the impact of context width on anomaly detection accuracy by
evaluating the accuracy of a given kNN anomaly detection problem on a
single sequence.
"""

CONTEXT_WIDTHS = range(20, 400, 1)
TEST_FILE = 'sequences/random_walk_added_noise'

# set up anomaly detectors
anomaly_detectors = []
ad_config = defaults.DEFAULT_KNN_CONFIG
for context_width in CONTEXT_WIDTHS:
    ad_config['context_config'] = {'method': 'local_symmetric', 'width': context_width}
    anomaly_detectors.append(anomaly_detection.create_anomaly_detector(**ad_config))

# init test
test = [utils.load_sequence(TEST_FILE)]
test_suite = utils.TestSuite(anomaly_detectors, CONTEXT_WIDTHS, [test], ['test'])

# execute test
test_suite.evaluate(display_progress=True)

# get plots
results = test_suite.results
fig1, plot1 = utils.plot_normalized_anomaly_vector_heat_map(results, CONTEXT_WIDTHS, ylabel='m')
fig2, plot2 = utils.plot_mean_error_values(results, CONTEXT_WIDTHS, CONTEXT_WIDTHS, xlabel='m')
fig3, plot3 = utils.plot_execution_times(results, CONTEXT_WIDTHS, CONTEXT_WIDTHS, xlabel='m')
