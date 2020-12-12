"""
Author: Alexander Fichtinger
"""

import numpy as np


class TestData:
    def __init__(self, feature_size: int, sample_size: int):
        self.data_array = self.create_random_data(feature_size, sample_size)

    def create_random_data(self, features: int, samples: int) -> np.ndarray:
        """ Create random data with a random normal distribution.

        The corresponding classes (0, 1) are randomly selected.

        :param features: int
        :param samples: int
        :return: np.ndarray
        """

        # normal distribution with µ = 0, variance = 25, SD = 5
        # ~95% between -2*5 = -10 and 2*5 = 10
        data_array = np.random.randn(samples, features + 1) * 5

        for sample in range(samples):
            np.random.seed(None)
            data_array[sample, -1] = np.random.choice([0, 1])

        return data_array
