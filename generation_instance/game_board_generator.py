"""
Author: Alexander Fichtinger
"""

from generation_instance.environment_interface import Environment
import numpy as np


class GameBoard(Environment):
    default_states = dict(
        OK=0,
        Trap=1,
        Monster=2,
        Goal=3
    )

    default_senses = np.array([
        'draft',    # when a trap is near
        'stench'    # when the monster is near
    ])

    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self.board = self.create_board(width, height)
        node_tuple = self.set_states(width, height)

        self.start_node = node_tuple[0]
        self.trap_node = node_tuple[1]
        self.monster_node = node_tuple[2]
        self.goal_node = node_tuple[3]

        self.board[self.trap_node[0], self.trap_node[1]] = 1
        self.board[self.monster_node[0], self.monster_node[1]] = 2
        self.board[self.goal_node[0], self.goal_node[1]] = 3

        senses = self.set_senses(width, height, self.trap_node, self.monster_node)

        self.draft_nodes = senses[0]
        self.stench_nodes = senses[1]

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
            rand_nodes_x = np.random.randint(1, width - 1, size=1)
            rand_nodes_y = np.random.randint(1, height - 1, size=1)

            monster_node = [start_node[0] + rand_nodes_y[0], start_node[1] + rand_nodes_x[0]]

        trap_node = monster_node

        while trap_node == gold_node or trap_node == start_node or trap_node == monster_node:
            rand_nodes_x = np.random.randint(0, width, size=1)
            rand_nodes_y = np.random.randint(0, height, size=1)

            trap_node = [rand_nodes_y[0], rand_nodes_x[0]]

        return start_node, trap_node, monster_node, gold_node

    def check_nodes(self, node: list, width: int, height: int) -> list:
        out_list = []

        if node[0] > 0:
            out_list.append([node[0] - 1, node[1]])
        if node[0] < height - 1:
            out_list.append([node[0] + 1, node[1]])
        if node[1] > 0:
            out_list.append([node[0], node[1] - 1])
        if node[1] < width - 1:
            out_list.append([node[0], node[1] + 1])

        return out_list

    def set_senses(self, width: int, height: int, trap_node: list, monster_node: list) -> tuple:
        draft_nodes = self.check_nodes(trap_node, width, height)
        stench_nodes = self.check_nodes(monster_node, width, height)

        return draft_nodes, stench_nodes


if __name__ == '__main__':
    obj = GameBoard(5, 5)
