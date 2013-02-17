# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='anomaly_detection',
    version='0.1',
    description='Anomaly detection on sequences.',
    long_description=readme,
    license=license,
    requires=['scipy', 'numpy', 'sklearn', 'mlpy', 'matplotlib'],
    packages=find_packages()
)
