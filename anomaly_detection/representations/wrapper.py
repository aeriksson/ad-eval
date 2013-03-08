

def wrap_evaluation_filter(evlauation_filter, converter):
    '''
    Wrapper for evaluation filters that converts their output series to a
    given representation (given by converter) before training/evaluating.
    '''
    def wrapper(sequence):
        for subsequence, start, end in evaluation_filter(sequence):
            yield converter(subsequence), start, end
    return wrapper


def wrap_reference_filter(reference_filter, converter):
    '''
    Wrapper for reference filters that converts their output sequences to a
    given representation (given by converter) before training/evaluating.
    '''
    def wrapper(sequence):
        for subsequence in reference_filter(sequence):
            yield converter(subsequence)
    return wrapper
