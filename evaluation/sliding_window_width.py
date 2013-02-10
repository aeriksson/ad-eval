import anomaly_detection
import utils

import defaults

"""
Visualizes the impact of the sliding window width on anomaly detection accuracy
by evaluating the accuracy of a given (sliding window) kNN anomaly detection
problem on a single sequence.
"""

WIDTH_VALUES = range(1, 101, 1)
TEST_FILE = 'sequences/random_walk_added_noise'

# set up anomaly detectors
anomaly_detectors = []
ad_config = defaults.DEFAULT_KNN_CONFIG
for width in WIDTH_VALUES:
    filter_config = {'method': 'sliding_window', 'width': width, 'step': 1}
    ad_config['evaluation_filter_config'] = filter_config
    ad_config['reference_filter_config'] = filter_config
    anomaly_detectors.append(anomaly_detection.create_anomaly_detector(**ad_config))

# init test
test = [utils.load_sequence(TEST_FILE)]
test_suite = utils.TestSuite(anomaly_detectors, WIDTH_VALUES, [test], ['test'])

# execute test
test_suite.evaluate(display_progress=True)

# get plot
results = test_suite.results
fig, plot = results.get_normalized_anomaly_vector_plot(WIDTH_VALUES)
plot.set_ylabel('sliding window width')

# rotate to get a better initial view
plot.azim = 120
plot.elev = 55

fig.show()
