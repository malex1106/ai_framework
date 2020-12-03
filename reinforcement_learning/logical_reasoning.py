"""
Author: Alexander Fichtinger
"""

from sympy import *
import dill as pickle


def entails(KB, state: str, next_node: list) -> bool:
    alpha = symbols(f'{state}{next_node[0]}_{next_node[1]}')
    check = And(KB, alpha)
    check = to_cnf(check)

    if satisfiable(check):
        return True
    else:
        return False


class logical_reasoning:
    def __init__(self, environment: dict):
        self.env = environment
        self.current_state = [0, 0]

    def create_clause(self, nodes: list, KB: object,
                      width: int, height: int,
                      state: str, sense: str) -> object:

        # no knowledge base and the senses have not perceived anything
        if KB is None and self.current_state not in nodes:
            KB = False

        # if the senses have perceived anything from the current state
        else:
            clause = symbols('False')               # empty clause
            t1 = t2 = t3 = t4 = symbols('False')    # set t1-t4 per default to False

            if self.current_state[0] > 0:
                t1 = symbols(f'{state}{self.current_state[0] - 1}_{self.current_state[1]}')
            if self.current_state[0] < height - 1:
                t2 = symbols(f'{state}{self.current_state[0] + 1}_{self.current_state[1]}')
            if self.current_state[1] > 0:
                t3 = symbols(f'{state}{self.current_state[0]}_{self.current_state[1] - 1}')
            if self.current_state[1] < width - 1:
                t4 = symbols(f'{state}{self.current_state[0]}_{self.current_state[1] + 1}')

            equal_sense = symbols(f'{sense}{self.current_state[0]}_{self.current_state[1]}')
            clause = Or(clause, t1, t2, t3, t4)
            clause = Implies(clause, equal_sense)

            # if the knowledge base is None => set it to true
            # otherwise the conjunction operator does not work
            if KB is None:
                KB = True

            KB = And(KB, clause)

        # if the knowledge base is not None and the senses have not perceived anything
        # just return the previous knowledge base
        # otherwise return the updated knowledge base
        return KB

    def check_kb(self, width: int, height: int, KB: object, next_node: list, sense: str):
        if sense == 'draft':
            nodes = self.env['draft_nodes']
            state = 'T'
            sense_type = 'D'
        elif sense == 'stengh':
            nodes = self.env['stengh_nodes']
            state = 'M'
            sense_type = 'S'
        else:
            raise TypeError('Wrong sense type!')

        # adopt and update current knowledge base
        KB = self.create_clause(nodes, KB, width, height, state, sense_type)

        # check for entailment and return an appropriate bool object
        return entails(KB, state, next_node)

    def train(self):
        width = self.env['width']
        height = self.env['height']

        KB = None

        check_draft = self.check_kb(width, height, KB, [1, 0], 'draft')
        check_stengh = self.check_kb(width, height, KB, [1, 0], 'stengh')

        if check_draft or check_stengh:
            print('Proof unsuccessfull! - 1')
        else:
            self.current_state = [1, 0]

        check_draft = self.check_kb(width, height, KB, [2, 0], 'draft')
        check_stengh = self.check_kb(width, height, KB, [2, 0], 'stengh')

        if check_draft or check_stengh:
            print('Proof unsuccessfull! - 2')
        else:
            self.current_state = [2, 0]


if __name__ == '__main__':
    with open('../test_data/board.pkl', 'rb') as f:
        data = pickle.load(f)

    print(data['board'])

    obj = logical_reasoning(data)
    obj.train()
