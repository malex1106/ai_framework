"""
Author: Alexander Fichtinger
"""

from generation_instance.environment_interface import Environment
import numpy as np


class Grid(Environment):
    default_actions = np.array([
        'down',
        'up',
        'right',
        'left',
        'stay'
    ])

    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self.gamma = 0.9

        # create general grid as a numpy array
        self.grid = self.create_board(width, height)
        self.start_node, self.terminal_node = self.set_states(width, height)
        self.rewards = self.define_rewards(self.terminal_node, width, height)

    def create_board(self, width: int, height: int) -> np.ndarray:
        """ Generate and return a numpy array as grid

        :param width: int (row size)
        :param height: int (column size)
        :return: ndarray
        """

        return np.zeros(
            (height, width),
            dtype=np.int
        )

    def set_states(self, width: int, height: int) -> tuple:
        """ Compute start and terminal node

        This method will compute coordinate of the start and terminal node randomly. This objects will be returned.

        Structure of an coordinate: e.g. start_node = [y, x] or [row, column]

        :param grid: ndarray
        :param width: int
        :param height: int
        :return: tuple
        """

        rand_nodes_x = np.random.randint(0, width, size=1)
        rand_nodes_y = np.random.randint(0, height, size=1)

        start_node = [rand_nodes_y[0], rand_nodes_x[0]]
        terminal_node = start_node

        while start_node == terminal_node:
            rand_nodes_x = np.random.randint(0, width, size=1)
            rand_nodes_y = np.random.randint(0, height, size=1)

            terminal_node = [rand_nodes_y[0], rand_nodes_x[0]]

        return start_node, terminal_node

    def define_rewards(self, terminal_node: list, width: int, height: int) -> np.ndarray:
        """ Defines all possible rewards for the respective actions

        :param terminal_node: list [y, x] or [row, column]
        :param width: int
        :param height: int
        :return: ndarray
        """

        rewards = np.empty(
            (height, width, 5),
            dtype=object
        )
        rewards[:] = -1

        if terminal_node[1] - 1 >= 0:
            rewards[terminal_node[0], terminal_node[1] - 1, 2] = 100
        if terminal_node[1] + 1 < width:
            rewards[terminal_node[0], terminal_node[1] + 1, 3] = 100
        if terminal_node[0] - 1 >= 0:
            rewards[terminal_node[0] - 1, terminal_node[1], 0] = 100
        if terminal_node[0] + 1 < height:
            rewards[terminal_node[0] + 1, terminal_node[1], 1] = 100
        rewards[terminal_node[0], terminal_node[1], :] = 0

        return rewards
