from verify import verify_subsequence


def get_local_symmetric_context_function(width):
    """
    Returns a function that takes a sequence S and the indices I of a subseqeunce and returns the
    local assymetric context of that subsequence with the specified widths, i.e. the n items in S
    preceding and succeeding I in S, where n=left_width.
    """
    return get_local_asymmetric_context_function(width, width)


def get_local_asymmetric_context_function(left_width, right_width):
    """
    Returns a function that takes a sequence S and the indices I of a subseqeunce and returns the
    local assymetric context of that subsequence with the specified widths, i.e. the n items in S
    preceding I and the k items succeding I, where n=left_width and k=right_width.
    """
    left_width = int(left_width)
    right_width = int(right_width)

    def get_local_context(sequence, subsequence_start, subsequence_end):
        return _get_local_context(
            sequence,
            subsequence_start,
            subsequence_end,
            left_width,
            right_width
        )

    return get_local_context


def _get_local_context(sequence, subsequence_start, subsequence_end, left_width, right_width):
    
    verify_subsequence(sequence, subsequence_start, subsequence_end)
    
    left_context_start = max(0, subsequence_start - left_width)
    left_context_end = max(0, subsequence_start - 1)

    sequence_end = len(sequence) - 1
    right_context_start = min(sequence_end, subsequence_end + 1)
    right_context_end = min(sequence_end, subsequence_end + right_width)

    return [sequence[left_context_start:left_context_end], sequence[right_context_start:right_context_end]]
