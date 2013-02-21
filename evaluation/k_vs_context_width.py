"""
Evaluates a test on a kNN anomaly detector with different values
of k and window width and creates a heat map of the accuracy.
"""
import anomaly_detection
import eval_utils as utils
import random
from matplotlib import pyplot

import defaults

import pickle

rng = random.Random(4)

K_VALUES = range(1, 50, 1)
W_VALUES = range(1, 50, 1)
TEST_FILE = 'sequences/random_walk_added_noise'

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

ad_label_list = sum(ad_label_matrix, [])

test = [utils.load_sequence(TEST_FILE)]
test_suite = utils.TestSuite(anomaly_detectors, ad_label_list, [test], 'test')

#execute
#test_suite.evaluate(display_progress=True)

results = test_suite.results

f = open('results.tmp', 'r+')
#pickle.dump(results, f)
results = pickle.load(f)
f.close()

# plot the distances
ERRORS = ['equal_support_distance', 'full_support_distance', 'normalized_euclidean_distance']
ERROR_LABELS = ['Equal support', 'Full support', 'Normalized Euclidean']

for error in ERRORS:
    utils.plots.plot_average_value_heat_map(results, ad_label_matrix, K_VALUES,
                                            W_VALUES, error, 'k', 'w')


# plot the anomaly vectors which minimize the distance measures
def get_label_of_n_smallest_key_value(distance_key, n):
    avgs = results.get_anomaly_detector_averages(ad_label_list, distance_key)
    sorted_avgs = sorted(zip(avgs, ad_label_list), key=lambda (a, b): a)
    return sorted_avgs[n][1]


fig = pyplot.figure()
plots = [fig.add_subplot(2, 2, i + 1) for i in range(4)]
ns = [1, 10, 50, 100]
for n, plot in zip(ns, plots):
    mins = [get_label_of_n_smallest_key_value(x, n) for x in ERRORS]
    title = "n = %s" % n
    utils.plots.plot_anomaly_vectors(results, mins, ERROR_LABELS, title=title, plot=plot, normalize=True)

fig.show()
