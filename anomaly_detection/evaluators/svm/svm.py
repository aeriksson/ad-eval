'''
SVM-based evaluator. Buffers training data.
'''

from sklearn import svm


class SVMEvaluator(object):

    def __init__(self, kernel="rbf", nu=0.1, gamma=0.1, **kwargs):
        self._classifier = svm.OneClassSVM(kernel=kernel, nu=nu, gamma=gamma, **kwargs)
        self._buffer = []
        self._training = True

    def train(self, sequence, *args):
        self._buffer.append(sequence)

    def evaluate(self, sequence, *args):
        if self._training:
            self._training = False
            self._classifier.fit(self._buffer)
            del self._buffer

        cls = self._classifier.predict(sequence)
        return 0 if cls == 1 else 1

    def uses_discrete_distance(self):
        return False
