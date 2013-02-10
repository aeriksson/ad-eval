from verify import verify_subsequence


def trivial_context_function(sequence, subsequence_start, subsequence_end):
    """
    Takes a sequence S and the indices I of a subseqeunce and returns the
    trivial context of that subsequence, i.e. all other elements in S.
    """
    verify_subsequence(sequence, subsequence_start, subsequence_end)
    
    left_context_start = 0
    left_context_end = max(0, subsequence_start - 1)

    sequence_end = len(sequence) - 1
    right_context_start = min(sequence_end, subsequence_end + 1)
    right_context_end = sequence_end

    return [sequence[left_context_start:left_context_end], sequence[right_context_start:right_context_end]]
