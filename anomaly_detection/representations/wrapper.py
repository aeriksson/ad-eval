'''
Wrapper for extractors that converts their output series
to a given representation before training/evaluating.
'''


def wrap_evaluation_filter(filter_generator, converter):
    def wrapper(sequence):
        for subsequence, start, end in filter_generator(sequence):
            yield converter(subsequence), start, end
    return wrapper


def wrap_reference_filter(filter_generator, converter):
    def wrapper(sequence):
        for subsequence in filter_generator(sequence):
            yield converter(subsequence)
    return wrapper
