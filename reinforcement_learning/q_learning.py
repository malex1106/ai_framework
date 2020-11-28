"""
Author: Alexander Fichtinger
"""

import numpy as np
from tqdm import tqdm
import dill as pickle


def e_greedy(rng, q, epsilon, actions, state) -> str:
    """ Epsilon-greedy function

    The epsilon-greedy function will take the action with the max rewards or a random action.
    Depending on the epsilon value, the probability can be changed.

    :param rng: numpy randomstate
    :param q: dict
    :param epsilon: float
    :param actions: float
    :param state: list
    :return: str
    """

    if rng.uniform(0, 1) > epsilon:
        index = int(rng.randint(len(actions), size=1))
        return actions[index]
    else:
        used_action = None
        best_action_value = float('-Inf')

        for action in actions:
            if q[(state[0], state[1], action)] > best_action_value:
                used_action = action
                best_action_value = q[(state[0], state[1], action)]

        return used_action


class q_learning:
    def __init__(self, environment: dict):
        self.env = environment
        self.current_state = self.reset()

    def reset(self) -> list:
        """ Reset the environment

        This method will reset the environment to the start conditions and
        return the start state.

        :return:
        """

        self.current_state = self.env['start_node']
        return self.current_state

    def step(self, action: str) -> tuple:
        """ Compute next steps

        This method will calculate the next state according to the current state
        and the action which was taken. In the case, that the next state equals the
        current one, the tuple (None, None, None) will be returned.
        In general, the return parameter is (next_state, reward, done).

        :param action: str
        :return: tuple
        """

        action_index = np.where(self.env['actions'] == action)
        next_state = self.current_state.copy()

        if action == 'down' and next_state[0] < self.env['height'] - 1:
            next_state[0] += 1
        elif action == 'up' and next_state[0] > 0:
            next_state[0] -= 1
        elif action == 'right' and next_state[1] < self.env['width'] - 1:
            next_state[1] += 1
        elif action == 'left' and next_state[1] > 0:
            next_state[1] -= 1
        else:
            return None, None, None

        reward = int(self.env['rewards'][self.current_state[0], self.current_state[1], action_index])
        terminal_node = self.env['terminal_node']

        if terminal_node == next_state:
            done = True
        else:
            done = False

        self.current_state = next_state

        return next_state, reward, done

    def train(self) -> dict:
        """ Update Q table

        This method updates the Q table, to learn [the shortest] a way for reaching
        the final state. The resulting Q table will be returned.

        ______

        Formula for calculating Q:

        Q(s,a) = Q(s,a) + alpha * [R(s,a) + gamma * max(Q(delta(s',a'), under all possible actions a')) - Q(s,a)]

        ______

        where

        Q(s,a) -> current Q value |
        R(s,a) -> reward function (applying action a on state s) |
        delta(s,a) -> state transition function (gives resulting state after action) |
        alpha -> learning rate |
        gamma -> discount factor

        :return: dict
        """

        # initialisations
        rng = np.random.RandomState(1234)
        alpha = 0.3
        epsilon = 0.3
        gamma = self.env['gamma']

        width = self.env['width']
        height = self.env['height']
        actions = self.env['actions']

        episodes = [int(i) for i in range(10000)]

        # create Q table as dictionary
        Q = dict()

        for row in range(height):
            for column in range(width):
                for action in actions:
                    Q[(row, column, action)] = 0

        # loop through episodes
        for _ in tqdm(episodes, total=len(episodes), desc="Computing..."):

            state = self.reset()

            while True:
                used_action = e_greedy(rng, Q, epsilon, actions, state)
                next_state, reward, done = self.step(used_action)

                # if next_state is None => action was not valid
                if next_state is None:
                    continue

                # all possible actions of the next state and their rewards are examined
                max_Q = -1
                for q_a in actions:
                    max_Q = max(Q[(next_state[0], next_state[1], q_a)], max_Q)

                # update Q-table
                Q[(state[0], state[1], used_action)] += \
                    alpha * (reward + gamma * max_Q - Q[(state[0], state[1], used_action)])

                # check for final state
                if done:
                    break

                state = next_state

        return Q


if __name__ == '__main__':
    with open('../test/grid.pkl', 'rb') as f:
        data = pickle.load(f)

    q = q_learning(data)
    q.train()
