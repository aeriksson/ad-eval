ad-eval - easy evaluation of sequential anomaly detection methods
===================================================================
A minimalistic and flexible framework optimized for efficient evaluation and comparison of anomaly detection methods (and problem formulations) on sets of sequential data.

This package was developed as a reaction to the general lack in the literature of objective and useful comparisons of anomaly detection methods for continuous time series. The anomaly detection packages has been designed to be highly flexible and can easily be adopted to encompass most (all?) existing methods, while the provided evaluation tools can be used to easily perform unbiased investigation into method strengths and weaknesses.

As it stands, the code is focused on detecting anomalies in continuous univariate time series, but it could easily be modified to handle other types of sequences. A one class SVM and kNN methods are included, along with various transformations and distance measures. 

Prerequisites
-------------
Python 2.7 with numpy, scikits.learn and matplotlib. 

Getting Started
---------------
Install the package by using the provided setup.py scrip, for instance by running ```python setup.py install``` (or, if you plan on modifying the code, by using ```pip --editable```).

A configurable UNIX-style executable that uses the anomaly detection package to perform anomaly detection is found at bin/anomaly_detector. Using this should be relatively straight-forward and is probably a good way of getting started.

Overview
--------
The main part of the project is the anomaly_detection package, which contains all the anomaly detection code and is highly configurable.

This package can be used to perform anomaly detection through the bin/anomaly_detector executable.

Finally, a comprehensive library for evaluation of different methods is provided in the evaluation/utils/ package. A few scripts that use this package to evaluate various aspects of anomaly detection methods are found in evaluation/.
