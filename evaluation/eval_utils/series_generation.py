from __future__ import division
import random


def generate_random_walk(length, mean, stdev, random_number_generator=None):
    """Generate a random walk.

    Generates a 1D random walk of the specified length and with the specified
    mean and standard deviation, where the first element is 0.
    """

    if random_number_generator is None:
        random_number_generator = random.Random()

    previous_state = 0
    walk = []
    for _ in range(length):
        current_state = previous_state + random_number_generator.gauss(mean, stdev)
        previous_state = current_state
        walk.append(current_state)
    return walk


def generate_bridged_random_walk(length, mean, stdev, random_number_generator=None):
    """Generate a Brownian bridge.

    Generates a 1D random walk of the specified length and with the specified
    mean and standard deviation, where the first and last elements are both 0.
    """
    walk = generate_random_walk(length, mean, stdev, random_number_generator)
    for i in range(length):
        walk[i] = walk[i] - (walk[-1] - walk[0]) * i / length
    return walk
