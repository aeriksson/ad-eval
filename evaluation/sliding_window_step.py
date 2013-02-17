import anomaly_detection
import utils

import defaults

"""
Visualizes the impact of the sliding window step on anomaly detection accuracy
by evaluating the accuracy of a given (sliding window) kNN anomaly detection
problem on a single sequence.
"""

STEP_VALUES = range(1, 11, 1)
TEST_FILE = 'sequences/random_walk_added_noise'

# set up anomaly detectors
anomaly_detectors = []
ad_config = defaults.DEFAULT_KNN_CONFIG
for step_value in STEP_VALUES:
    filter_config = {'method': 'sliding_window', 'width': 10, 'step': step_value}
    ad_config['evaluation_filter_config'] = filter_config
    ad_config['reference_filter_config'] = filter_config
    anomaly_detectors.append(anomaly_detection.create_anomaly_detector(**ad_config))

# init test
test = [utils.load_sequence(TEST_FILE)]
test_suite = utils.TestSuite(anomaly_detectors, STEP_VALUES, [test], ['test'])

# execute test
test_suite.evaluate(display_progress=True)

# get plots
results = test_suite.results
fig1, plot1 = utils.plot_normalized_anomaly_vector_heat_map(results, STEP_VALUES, ylabel='s')
fig2, plot2 = utils.plot_mean_error_values(results, STEP_VALUES, STEP_VALUES, xlabel='s')
fig3, plot3 = utils.plot_execution_times(results, STEP_VALUES, STEP_VALUES, xlabel='s')
