"""
Author: Alexander Fichtinger
"""

import numpy as np
import matplotlib.pyplot as plt

from decision_trees.id3 import TreeNode


def setup_subplots(subplot: plt.subplot, color: str, title: str, x_label: str, y_label: str):
    """ Configure subplots.

    :param subplot: plt.subplot
    :param width: int
    :param height: int
    :param color: str
    :param title: str
    """

    subplot.xaxis.tick_top()
    subplot.grid(color=color, linestyle='-', linewidth=1)
    subplot.set_aspect('equal', adjustable='box')
    subplot.set_title(title)
    subplot.set_xlabel(x_label)
    subplot.set_ylabel(y_label)


def construct_tree(root_node: TreeNode, split_list: list):
    if root_node.terminal is not None:
        return split_list
    else:
        split_list.append(root_node.split_point)
        split_list = construct_tree(root_node.left_child, split_list)
        split_list = construct_tree(root_node.right_child, split_list)

        return split_list


def setup_interface(data: dict):
    tree_node = data['root_node']
    data_points = np.asarray(data['data'])
    class_0_list = []
    class_1_list = []

    for sample in data_points:
        if sample[-1] == 0:
            class_0_list.append(sample.tolist())
        elif sample[-1] == 1:
            class_1_list.append(sample.tolist())

    class_0_array = np.asarray(class_0_list)
    class_1_array = np.asarray(class_1_list)

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(10, 6, forward=True)

    plt.plot(class_0_array[:, 0], class_0_array[:, 1], 'o', color='blue', label='class 0')
    plt.plot(class_1_array[:, 0], class_1_array[:, 1], 'x', color='red', label='class 1')
    plt.legend(numpoints=1)

    split_points = construct_tree(tree_node, [])


    for (feature, split_at) in split_points:
        if feature == 0:
            plt.axvline(x=split_at, ymin=min(data_points[:, 0]), ymax=max(data_points[:, 0]))
        elif feature == 1:
            plt.axhline(y=split_at, xmin=min(data_points[:, 1]), xmax=max(data_points[:, 1]))

    setup_subplots(ax, 'white', 'Data points', 'feature 0', 'feature 1')