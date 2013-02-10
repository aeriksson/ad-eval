import anomaly_detection
import utils
import random

import defaults

"""
Evaluates a test on a kNN anomaly detector with different values
of k and window width and creates a heat map of the accuracy.
"""

rng = random.Random()

K_VALUES = range(1, 100, 10)
W_VALUES = range(1, 100, 10)

# generate anomaly_detectors
ad_config = defaults.DEFAULT_KNN_CONFIG
anomaly_detectors = []
ad_label_matrix = []
for k in K_VALUES:
    ad_row = []
    for w in W_VALUES:
        ad_config['evaluator_config']['k'] = k
        ad_config['evaluation_filter_config']['width'] = w
        ad_config['reference_filter_config']['width'] = w
        ad = anomaly_detection.create_anomaly_detector(**ad_config)
        anomaly_detectors.append(ad)
        ad_row.append(str(k) + ',' + str(w))
    ad_label_matrix.append(ad_row)

# generate test
test_config = {'count': 1, 'amplitude_interval': [0.0, 1.0], 'width_interval': [5, 40], 'anomaly_type': 'noise'}
base_sequence = utils.generate_bridged_random_walk(400, 0, 0.1, rng)
test = utils.generate_random_test(base_sequence, random_number_generator=rng, **test_config)

test_suite = utils.TestSuite(anomaly_detectors, sum(ad_label_matrix, []), [test], 'test')

#execute
test_suite.evaluate(display_progress=True)

results = test_suite.results

fig, plot = results.get_average_value_plot(ad_label_matrix, K_VALUES, W_VALUES, 'equal_support_distance')
plot.set_xlabel('k')
plot.set_ylabel('w')

fig.show()
