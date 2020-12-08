"""
Author: Alexander Fichtinger
"""

import dill as pickle


def check_for_duplicates(input_list: list) -> list:
    """ Check for duplicates.

    :param input_list: list
    :return: unique list
    """

    return [i for n, i in enumerate(input_list) if i not in input_list[:n]]


def check_for_neighbours(state: list, width: int, height: int) -> list:
    """ Calculate all neighbours.

    :param state: list
    :param width: int
    :param height: int
    :return: list
    """

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
    """ Compare all neighbours of visited states if a sense has struck.

    If two states have the same possible trap/monster states as neighbours,
    then the trap/monster is among the same neighbors (=> saved in 'avoidance')

    :param knowledge_base: dict
    :param sense_assumption: list
    :return: dict
    """

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

            # check for similar neighbours
            find_similar = [x for x in inner_next_states + inner_selected_states
                            if x in inner_next_states and
                            x in inner_selected_states and
                            x not in knowledge_base['visited_nodes']]

            find_similar = check_for_duplicates(find_similar)

            # save similiar assumptions one level higher ('avoidance')
            if len(find_similar) > 0:
                new_assumptions = new_assumptions + find_similar
                found_same_assumption = True

            # remove assumptions from hypothesis ('possible_traps/monsters')
            if _ not in delete_assumptions:
                delete_assumptions.append(_)
            if counter not in delete_assumptions:
                delete_assumptions.append(counter)

    # update the possible states
    for ele in sorted(delete_assumptions, reverse=True):
        del sense_assumption[ele]

    # if two states have the same neighbours
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

    def step(self, next_state: list, KB: dict, width: int, height: int) -> dict:
        """ Check the next state and update the current state if necessary.

        :param next_state: list
        :param KB: dict
        :param width: int
        :param height: int
        :return: dict
        """

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
                KB['possible_traps'].append(neighbours.copy())
                no_draft = False
            if self.current_state in self.stench_nodes:
                KB['possible_monsters'].append(neighbours.copy())
                no_stench = False

            # if nothing was detected => check whether neighbors are wrongly ignored
            if no_draft or no_stench:
                for neighbour in neighbours:
                    if neighbour in KB['avoidance']:
                        KB['avoidance'].remove(neighbour)
            if no_draft:
                for node_assum in KB['possible_traps']:
                    for neighbour in neighbours:
                        if neighbour in node_assum:
                            node_assum.remove(neighbour)
            if no_stench:
                for node_assum in KB['possible_monsters']:
                    for neighbour in neighbours:
                        if neighbour in node_assum:
                            node_assum.remove(neighbour)

            # compare assumptions and calculate states which should be ignored
            KB = check_assumptions(KB, KB['possible_traps'])
            KB = check_assumptions(KB, KB['possible_monsters'])

        contr_assumptions = True

        # check for possible traps
        for inner_element in KB['possible_traps']:
            if next_state in inner_element:
                contr_assumptions = False

        # check for possible monsters
        for inner_element in KB['possible_monsters']:
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

    def train(self) -> tuple:
        """ Compute the next state, check for gold state and return the final results.

        :return: tuple (knowledge_base: dict, gold state: list)
        """

        width = self.env['width']
        height = self.env['height']

        KB = dict(
            visited_nodes=[],
            possible_traps=[],
            possible_monsters=[],
            avoidance=[]
        )

        while True:
            neighbours = check_for_neighbours(self.current_state, width, height)

            self.queue = self.queue + neighbours
            self.queue = check_for_duplicates(self.queue)

            next_state = self.queue.pop(0)

            KB = self.step(next_state, KB, width, height)

            if self.current_state == self.env['goal_node']:
                break
            elif self.current_state == self.env['trap_node'] or \
                    self.current_state == self.env['monster_node']:
                raise Exception('PLAYER DIED!')
        """
        for value in KB.items():
            print(value)
        """

        return KB, self.current_state


if __name__ == '__main__':
    with open('../test_data/board.pkl', 'rb') as f:
        data = pickle.load(f)

    print(data['board'])

    obj = LogicalReasoning(data)
    obj.train()
