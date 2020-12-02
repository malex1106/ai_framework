"""
Author: Alexander Fichtinger
"""

from generation_instance.environment_interface import Environment
import numpy as np


class GameBoard(Environment):
    default_states = dict(
        O=0,    # 0 for OK
        T=1,    # 1 for Trap
        M=2,    # 2 for Monster
        G=3     # 3 for Gold
    )

    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self.board = self.create_board(width, height)
        node_tuple = self.set_states(width, height)

        self.start_node = node_tuple[0]
        self.start_node = node_tuple[0]
        self.start_node = node_tuple[0]
        self.start_node = node_tuple[0]

        print(self.board)
        print(node_tuple)

    def create_board(self, width: int, height: int) -> np.ndarray:
        return np.zeros(
            (height, width),
            dtype=np.int
        )

    def set_states(self, width: int, height: int) -> tuple:
        rand_nodes = np.random.randint(0, 2, size=2)
        start_node = [0 + rand_nodes[0], 0 + rand_nodes[1]]

        rand_nodes = np.random.randint(1, 3, size=2)
        gold_node = [height - rand_nodes[0], width - rand_nodes[1]]

        monster_node = gold_node

        while monster_node == gold_node or monster_node == start_node:
            rand_nodes_x = np.random.randint(0, width, size=1)
            rand_nodes_y = np.random.randint(0, height, size=1)

            monster_node = [rand_nodes_y[0], rand_nodes_x[0]]

        trap_node = monster_node

        while trap_node == gold_node or trap_node == start_node or trap_node == monster_node:
            rand_nodes_x = np.random.randint(0, width, size=1)
            rand_nodes_y = np.random.randint(0, height, size=1)

            trap_node = [rand_nodes_y[0], rand_nodes_x[0]]

        return start_node, trap_node, monster_node, gold_node


if __name__ == '__main__':
    obj = GameBoard(5, 5)
