from __future__ import division
from sys import stdout


class ProgressCounter():
    """
    Keeps track of anomaly detector/test/sequence progress.
    """
    def __init__(self, total_detectors=1, completed_detectors=0, total_tests=1,
                 completed_tests=0, total_sequences=1, completed_sequences=0,
                 sequence_progress=0):
        self.total_detectors = total_detectors
        self.completed_detectors = completed_detectors
        self.total_tests = total_tests
        self.completed_tests = completed_tests
        self.total_sequences = total_sequences
        self.completed_sequences = completed_sequences
        self.sequence_progress = sequence_progress

    def print_progress(self):
        format_string = "\rrunning test... "

        format_string += self._generate_counter_string(
            "anomaly detectors",
            self.total_detectors,
            self.completed_detectors
        )
        format_string += self._generate_counter_string(
            "tests",
            self.total_tests,
            self.completed_tests
        )
        format_string += self._generate_counter_string(
            "sequences",
            self.total_sequences,
            self.completed_sequences
        )
        format_string += 'current sequence %s%%' % (100.0 * self.sequence_progress)

        stdout.write(format_string)
        stdout.flush()

    def _generate_counter_string(self, name, total, completed):
        return "{} {: >.1%} ({}/{}), ".format(name, completed / total, completed, total)
