_SUBSEQUENCE_ORDER_ERROR = 'Subsequence order is wrong: [%s, %s].'
_SUBSEQUENCE_BOUNDS_ERROR = 'Subsequence [%s, %s] not in sequence interval [%s, %s].'


def verify_subsequence(sequence, start, end):
    """
    Verifies that the given interval ([start, end]) is valid and is contained in the interval
    given by the sequence.
    """
    assert start <= end, _SUBSEQUENCE_ORDER_ERROR % (start, end)
    sequence_end = len(sequence) - 1
    assert start >= 0 and end <= sequence_end, _SUBSEQUENCE_BOUNDS_ERROR % (start, end, 0, sequence_end)
