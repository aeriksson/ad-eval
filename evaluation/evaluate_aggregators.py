import anomaly_detection
import eval_utils as utils
import random

rng = random.Random()

filter_config = {'method': 'sliding_window', 'width': 10, 'step': 1}
context_config = {'method': 'local_symmetric', 'width': 100}
evaluator_config = {'method': 'knn', 'distance_measure': 'euclidean'}
aggregator_configs = [{'method': 'max'}, {'method': 'mean'}, {'method': 'median'}]

aggregator_types = ['max', 'mean', 'median']
anomaly_types = ['noise', 'sine']

# generate anomaly_detectors
anomaly_detectors = []
for aggregator_type in aggregator_types:
    aggregator_config = {'method': aggregator_type}
    anomaly_detector = anomaly_detection.create_anomaly_detector(
        filter_config,
        context_config,
        filter_config,
        evaluator_config,
        aggregator_config
    )
    anomaly_detectors.append(anomaly_detector)

# generate tests
tests = []
test_config = {'count': 100, 'amplitude_interval': [0.0, 1.0], 'width_interval': [5, 20]}
for anomaly_type in anomaly_types:
    test_config['anomaly_type'] = anomaly_type
    base_sequence = utils.generate_bridged_random_walk(100, 0, 0.1, rng)
    test = utils.generate_random_test(base_sequence, random_number_generator=rng, **test_config)
    tests.append(test)

test_suite = utils.TestSuite(anomaly_detectors, aggregator_types, tests, anomaly_types, 'aggregator test')

#execute
test_suite.evaluate(display_progress=True)
test_suite.print_report()
