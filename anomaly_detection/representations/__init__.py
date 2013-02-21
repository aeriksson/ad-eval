from sax import get_sax_converter
from dft import get_dft_converter
from dwt import get_dwt_converter
from z_normalize import get_z_normalization_converter

from wrapper import wrap_evaluation_filter, wrap_reference_filter


def get_representation_converter(method, dimensions=None, alphabet_size=None, **kwargs):
    if method == 'sax':
        return get_sax_converter(dimensions=int(dimensions), alphabet_size=int(alphabet_size), **kwargs)
    elif method == 'dft':
        return get_dft_converter(**kwargs)
    elif method == 'dwt':
        return get_dwt_converter(**kwargs)
    elif method == 'z-normalize':
        return get_z_normalization_converter()
    else:
        raise NotImplementedError('Method "%s" not implemented.' % method)
