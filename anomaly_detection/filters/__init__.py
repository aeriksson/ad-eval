from sliding_window import sliding_window_filter, sliding_window_reference_filter
 

def get_evaluation_filter(method='sliding_window', **kwargs):
    if method == 'sliding_window':
        return lambda time_series: sliding_window_filter(time_series, **kwargs)
    else:
        raise NotImplementedError('Evaluation filter "%s" not implemented' % method)


def get_reference_filter(method='sliding_window', **kwargs):
    if method == 'sliding_window':
        return lambda time_series: sliding_window_reference_filter(time_series, **kwargs)
    else:
        raise NotImplementedError('Reference filter "%s" not implemented' % extractor)
