"""
Author: Alexander Fichtinger
"""

from utils.logical_operations import LogicalOperator
import dill as pickle
import numpy as np
import time
from sympy import *


def check_for_duplicates(input_list: list) -> list:
    return [i for n, i in enumerate(input_list) if i not in input_list[:n]]


def check_for_neighbours(state: list, width: int, height: int) -> list:
    row, column = state[0], state[1]
    neighbours = []

    if row > 0:
        neighbours.append([row - 1, column])
    if row < height - 1:
        neighbours.append([row + 1, column])
    if column > 0:
        neighbours.append([row, column - 1])
    if column < width - 1:
        neighbours.append([row, column + 1])

    return neighbours


def check_assumptions(knowledge_base: dict, sense_assumption: list) -> dict:
    new_assumptions = []
    delete_assumptions = []
    found_same_assumption = False

    # due to the 3d likely structure, 3 loops are needed
    # maybe this could be improved

    # take every assumption in a row
    for counter, nested_list in enumerate(sense_assumption):
        inner_selected_states = [i for i in nested_list]

        # compare it with all other assumptions
        for _ in range(counter + 1, len(sense_assumption)):
            inner_next_states = [i for i in sense_assumption[_]]

            # check all states
            for state in inner_next_states:
                if state in inner_selected_states:
                    if state not in knowledge_base['visited_nodes']:
                        new_assumptions.append(state)
                    if _ not in delete_assumptions:
                        delete_assumptions.append(_)
                    if counter not in delete_assumptions:
                        delete_assumptions.append(counter)
                    found_same_assumption = True

    for ele in sorted(delete_assumptions, reverse=True):
        del sense_assumption[ele]

    if found_same_assumption:
        knowledge_base['avoidance'] = knowledge_base['avoidance'] + new_assumptions
        knowledge_base['avoidance'] = check_for_duplicates(knowledge_base['avoidance'])

    return knowledge_base


class LogicalReasoning:
    def __init__(self, environment: dict):
        self.env = environment
        self.current_state = environment['start_node']
        self.draft_nodes = self.env['draft_nodes']
        self.stench_nodes = self.env['stench_nodes']
        self.queue = []

    def step(self, next_state: list, KB: dict, width: int, height: int):
        # compute assumptions only once
        if self.current_state not in KB['visited_nodes']:

            # update visited list
            KB['visited_nodes'].append(self.current_state)

            # some initializations
            no_draft = True
            no_stench = True
            neighbours = check_for_neighbours(self.current_state, width, height)

            # check senses
            if self.current_state in self.draft_nodes:
                KB['draft_assumptions'].append(neighbours.copy())
                no_draft = False
            if self.current_state in self.stench_nodes:
                KB['stench_assumptions'].append(neighbours.copy())
                no_stench = False

            # if nothing was detected => check whether neighbors are wrongly ignored
            if no_draft or no_stench:
                for neighbour in neighbours:
                    if neighbour in KB['avoidance']:
                        KB['avoidance'].remove(neighbour)

            # compare assumptions and calculate states which should be ignored
            KB = check_assumptions(KB, KB['draft_assumptions'])
            KB = check_assumptions(KB, KB['stench_assumptions'])

        contr_assumptions = True

        # check for possible traps
        for inner_element in KB['draft_assumptions']:
            if next_state in inner_element:
                contr_assumptions = False

        # check for possible monsters
        for inner_element in KB['stench_assumptions']:
            if next_state in inner_element:
                contr_assumptions = False

        # check for possible traps/monster on a higher computation level
        if next_state in KB['avoidance']:
            contr_assumptions = False

        # set new state
        if contr_assumptions or next_state in KB['visited_nodes']:
            self.current_state = next_state
        elif next_state in KB['visited_nodes']:
            self.current_state = next_state
        else:
            self.queue.append(next_state)

        KB['visited_nodes'] = check_for_duplicates(KB['visited_nodes'])

        return KB

    def train(self):
        width = self.env['width']
        height = self.env['height']

        KB = dict(
            visited_nodes=[],
            draft_assumptions=[],
            stench_assumptions=[],
            avoidance=[]
        )

        print(f'Start state: {self.current_state}')

        while True:
            neighbours = check_for_neighbours(self.current_state, width, height)

            self.queue = self.queue + neighbours
            self.queue = check_for_duplicates(self.queue)

            next_state = self.queue.pop(0)

            KB = self.step(next_state, KB, width, height)

            #print(f'Current state: {self.current_state}, Next state: {self.queue[0]}')

            if self.current_state == self.env['goal_node']:
                break
            elif self.current_state == self.env['trap_node'] or \
                    self.current_state == self.env['monster_node']:
                raise Exception('PLAYER DIED!')

        print(f'End state: {self.current_state}')
        for data in KB.items():
            print(data)


if __name__ == '__main__':
    with open('../test_data/board.pkl', 'rb') as f:
        data = pickle.load(f)

    print(data['board'])

    obj = LogicalReasoning(data)
    obj.train()
