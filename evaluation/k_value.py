import anomaly_detection
import utils

import defaults

"""
Visualizes the impact of the kNN k values on anomaly detection accuracy by
evaluating the accuracy of a given kNN anomaly detection problem on a
single sequence.
"""

K_VALUES = range(1, 101, 1)
TEST_FILE = 'sequences/random_walk_added_noise'

# set up anomaly detectors
anomaly_detectors = []
ad_config = defaults.DEFAULT_KNN_CONFIG
for k_value in K_VALUES:
    ad_config['evaluator_config']['k'] = k_value
    anomaly_detectors.append(anomaly_detection.create_anomaly_detector(**ad_config))

# init test
test = [utils.load_sequence(TEST_FILE)]
test_suite = utils.TestSuite(anomaly_detectors, K_VALUES, [test], ['test'])

# execute test
test_suite.evaluate(display_progress=True)

# get plots
results = test_suite.results
fig1, plot1 = utils.plot_normalized_anomaly_vector_heat_map(results, K_VALUES, ylabel='k')
fig2, plot2 = utils.plot_mean_error_values(results, K_VALUES, K_VALUES, xlabel='k')
fig3, plot3 = utils.plot_execution_times(results, K_VALUES, K_VALUES, xlabel='k')
