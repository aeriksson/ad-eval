from local_context import get_local_symmetric_context_function, get_local_asymmetric_context_function
from novelty_context import novelty_context_function
from trivial_context import trivial_context_function
from semisupervised_context import get_semisupervised_context_function


def get_context(
    method='local_symmetric',
    width='100',
    left_width=100,
    right_width=100,
    reference_sequence=[],
    **kwargs
):
    return {
        'local_symmetric': get_local_symmetric_context_function(width, **kwargs),
        'local_asymmetric': get_local_asymmetric_context_function(
                left_width=left_width,
                right_width=right_width,
                **kwargs
            ),
        'novelty': novelty_context_function,
        'trivial': trivial_context_function,
        'semi-supervised': get_semisupervised_context_function(reference_sequence)
    }[method]
