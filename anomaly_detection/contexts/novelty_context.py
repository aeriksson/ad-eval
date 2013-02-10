from verify import verify_subsequence


def novelty_context_function(sequence, subseqence_start, subsequence_end):
    """
    Takes a sequence S and the indices I of a subseqeunce and returns the
    novelty context of that subsequence, i.e. all elements preceding I in S.
    """
    verify_subsequence(sequence, subsequence_start, subsequence_end)
    
    context_start = max(0, subsequence_start - left_width)
    context_end = max(0, subsequence_start - 1)

    return [sequence[context_start, context_end]]
