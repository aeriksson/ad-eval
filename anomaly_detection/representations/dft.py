from scipy import fftpack


def get_dft_converter(**kwargs):
    return lambda time_series: fftpack.rfft(time_series)
