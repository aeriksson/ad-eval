import anomaly_detection
import utils

import defaults

"""
Visualizes the impact of the kNN k values on anomaly detection accuracy by
evaluating the accuracy of a given kNN anomaly detection problem on a
single sequence.
"""

K_VALUES = range(1, 100, 2)
TEST_FILE = 'sequences/random_walk_added_noise'

# set up anomaly detectors
anomaly_detectors = []
ad_config = defaults.DEFAULT_KNN_CONFIG
for k_value in K_VALUES:
    ad_config['evaluator_config'] = {'method': 'knn', 'distance_measure': 'euclidean', 'k': k_value}
    anomaly_detectors.append(anomaly_detection.create_anomaly_detector(**ad_config))

# init test
test = [utils.load_sequence(TEST_FILE)]
test_suite = utils.TestSuite(anomaly_detectors, K_VALUES, [test], ['test'])

# execute test
test_suite.evaluate(display_progress=True)

# get plot
results = test_suite.results
fig, plot = results.get_normalized_anomaly_vector_plot(K_VALUES)
plot.set_ylabel('k value')

# rotate to get a better initial view
plot.azim = 120
plot.elev = 55

fig.show()
