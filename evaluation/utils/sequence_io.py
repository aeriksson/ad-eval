import numpy


def load_sequence(path):
    '''
    Loads a sequence from the given path.

    The file can either be a single array or a 2D array containing two arrays
    of equal length.

    If the file is a single array, that array is returned.
    If the file consists of a 2D array containing two arrays, the first of
    these is assumed to be an evaluation sequence and the second an anomaly
    vector. Both of these must be of equal length.

    Arguments:
        path: Path to a valid file.

    Returns:
        A tuple consisting of the evaluation sequence and anomaly vector in
        the file. If no anomaly vector is found, the second element in the
        tuple is None.

    Raises:
        IOError: Invalid file.
    '''
    arr = numpy.load(path)
    try:
        dims = len(arr.shape)
        if dims == 1:
            return arr
        elif dims == 2:
            return arr[0], arr[1]
    except Error:
        raise IOError('Invalid file')


def save_sequence(path, sequence, anomaly_vector=None):
    '''
    Saves a sequence to the given path.

    Arguments:
        path: Path to a valid file.
        sequence: The sequence (assumed iterable).
        anomaly_vector: An optional anomaly vector.
    '''

    # open file in advance to prevent numpy from
    # appending '.npy' to the filename
    sequence_file = open(path, 'w')

    if anomaly_vector is None:
        numpy.save(sequence_file, sequence)
    else:
        numpy.save(sequence_file, [sequence, anomaly_vector])

    sequence_file.close()
