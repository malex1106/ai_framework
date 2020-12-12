"""
Author: Alexander Fichtinger
"""

import numpy as np
from scipy import stats


class TreeNode:
    def __init__(self):
        self.terminal = None
        self.split_point = None
        self.left_child = None
        self.right_child = None

    def __str__(self):
        if self.terminal is not None:
            return "(" + str(self.terminal) + ")"
        else:
            return f'[({self.split_point[0]}:{self.split_point[1]}) => {self.left_child} | ' \
                   f'{self.right_child}]'


def entropy(labels: np.ndarray):
    n = len(labels)
    if n == 0:
        return 0.0
    positive = np.count_nonzero(labels == 1.) / n
    negative = 1 - positive
    if positive == 0 or negative == 0:
        return 0.0
    # stats.entropy returns the same as
    # -positive * np.log2(positive) - negative * np.log2(negative)
    return stats.entropy([positive, negative], base=2)


class DecisionTree:
    def get_splits(self, data: np.ndarray) -> list:
        _, n_columns = data.shape
        split_points = []

        for column_index in range(n_columns - 1):
            values = data[:, column_index]
            unique_values = np.unique(values)

            for sample_index in range(len(unique_values)):
                if sample_index != 0:
                    current_value = unique_values[sample_index]
                    previous_value = unique_values[sample_index - 1]
                    split = (current_value + previous_value) / 2

                    split_points.append((column_index, split))

        return split_points

    def information_gain(self, data: np.ndarray, split_point: tuple) -> float:
        split_feature, split_at = split_point
        labels = data[:, -1]
        labels_left_split = []
        labels_right_split = []

        for sample_index in range(len(data)):
            split_data = data[sample_index, split_feature]

            if split_data <= split_at:
                labels_left_split.append(labels[sample_index])
            elif split_data > split_at:
                labels_right_split.append(labels[sample_index])

        general_entropy = entropy(labels)
        entropy_left_split = entropy(np.array(labels_left_split))
        entropy_right_split = entropy(np.array(labels_right_split))

        ig = general_entropy - len(labels_left_split) / len(labels) * entropy_left_split \
                             - len(labels_right_split) / len(labels) * entropy_right_split

        return ig

    def best_split_point(self, data: np.ndarray):
        split_feature, split_value = None, None
        all_splits = self.get_splits(data)
        best_ig = float('-Inf')

        for (feature_index, split_at) in all_splits:
            ig = self.information_gain(data, (feature_index, split_at))

            if ig > best_ig:
                best_ig = ig
                split_feature = feature_index
                split_value = split_at

        return split_feature, split_value

    def split_data(self, data) -> TreeNode():
        features = data[:, :-1]
        labels = data[:, -1]
        unique_labels = np.unique(labels)

        node = TreeNode()

        if len(unique_labels) == 1:
            node.terminal = unique_labels[0]
        else:
            split_feature, split_at = self.best_split_point(data)

            data_left = data[np.where(features[:, split_feature] <= split_at)]
            data_right = data[np.where(features[:, split_feature] > split_at)]

            node.left_child = self.split_data(data_left)
            node.right_child = self.split_data(data_right)

            node.split_point = (split_feature, split_at)

        return node
