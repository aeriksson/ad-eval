from scipy import fftpack


def get_dft_converter(**kwargs):
    """
    Returns a function that converts sequences to their DFT representations.
    """
    return lambda sequence: fftpack.rfft(sequence)
