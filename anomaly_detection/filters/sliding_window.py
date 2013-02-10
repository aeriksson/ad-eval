_TYPE_ERROR = 'width and step must be int but are %s and %s'
_WIDTH_ERROR = 'width must not be larger than sequence length.'


def sliding_window_reference_filter(context, width, step=1):
    """
    Context is assumed to be a list of sequences.
    These are iterated over to form a reference set.
    """

    reference_set = []

    for sequence in context:
        for subsequence, _, _ in sliding_window_filter(sequence, width, step):
            reference_set.append(subsequence)

    return reference_set


def sliding_window_filter(sequence, width, step=1):
    """
    Sliding window generator for sequences.
    """
    step = int(step)
    width = int(width)

    count = ((len(sequence) - width) / step) + 1

    for i in range(0, count * step, step):
        start = i
        end = i + width
        yield sequence[start: end], start, end - 1
