def get_semisupervised_context_function(reference_sequence):
    """
    Returns the semi-supervised context, which is always trivially the reference sequence.
    """
    return lambda seq, subseq_start, subseq_end: reference_sequence
