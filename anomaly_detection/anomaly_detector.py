from __future__ import division

import logging

import filters
import contexts
import evaluators
import aggregators
import representations

logger = logging.getLogger()

_INIT_MESSAGE = ('Anomaly detector created.'
                 'Evaluation filter: {evaluation_filter!s}, '
                 'context function: {context_function!s}, '
                 'reference filter: {reference_filter!s}, '
                 'evaluator: {evaluator!s}, '
                 'aggregator: {aggregator!s}.')
_EVALUATE_MESSAGE = 'Evaluating sequence {!s}.'
_ANOMALY_SCORES_MESSAGE = 'Obtained anomaly scores {!s}.'


def create_anomaly_detector(evaluation_filter_config, context_config, reference_filter_config,
                            evaluator_config, aggregator_config, representation_config=None,
                            discretization_config=None):
    """
    Creates an anomaly detector from a set of config dicts.
    See the individual modules for how to setup each of the config dicts.
    Representation and discretization configurations are optional.
    However, a discretization config is required if a discrete distance function is used.
    """
    evaluation_filter = filters.get_evaluation_filter(**evaluation_filter_config)
    context = contexts.get_context(**context_config)
    reference_filter = filters.get_reference_filter(**reference_filter_config)
    evaluator = evaluators.get_evaluator(**evaluator_config)
    aggregator = aggregators.get_aggregator(**aggregator_config)

    converter = _get_filter_wrapper(evaluator_config, representation_config, discretization_config)
    evaluation_filter = representations.wrap_evaluation_filter(evaluation_filter, converter)
    reference_filter = representations.wrap_reference_filter(reference_filter, converter)

    return AnomalyDetector(evaluation_filter, context, reference_filter, evaluator, aggregator)


def _get_filter_wrapper(evaluator_config, representation_config=None, discretization_config=None):
    wrapper = lambda x: x

    if representation_config is not None:
        r = representations.get_representation_converter(**representation_config)
        wrapper = r

    if evaluators.uses_discrete_distance(evaluator_config):
        r = representations.get_representation_converter(**discretization_config)
        new_wrapper = lambda x: r(wrapper(x))
        return new_wrapper

    return wrapper


class AnomalyDetector(object):

    def __init__(self, evaluation_filter, context_function, reference_filter,
                 evaluator, aggregator):
        self.reference_filter = reference_filter
        self.context_function = context_function
        self.evaluation_filter = evaluation_filter
        self.evaluator = evaluator
        self.aggregator = aggregator

        logger.info(_INIT_MESSAGE % {
            'reference_filter': reference_filter,
            'context_function': context_function,
            'evaluation_filter': evaluation_filter,
            'evaluator': evaluator,
            'aggregator': evaluation_filter,
        })

    def evaluate(self, evaluation_sequence, progress_callback=None):
        logger.debug(_EVALUATE_MESSAGE % evaluation_sequence)

        self.aggregator.init(len(evaluation_sequence))

        for sequence, start, end in self.evaluation_filter(evaluation_sequence):
            context = self.context_function(evaluation_sequence, start, end)
            reference_set = self.reference_filter(context)
            score = self.evaluator.evaluate(sequence, reference_set)
            self.aggregator.add_score(score, start, end)

            if progress_callback is not None:
                progress_callback(end / len(evaluation_sequence - (end - start)))

        anomaly_scores = self.aggregator.get_aggregated_scores()

        if progress_callback is not None:
            progress_callback(1)

        logger.debug(_ANOMALY_SCORES_MESSAGE % anomaly_scores)

        return anomaly_scores
