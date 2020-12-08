"""
Author: Alexander Fichtinger
"""

from reinforcement_learning.q_learning import QLearning
from reinforcement_learning.logical_reasoning import LogicalReasoning
import argparse
import os
import dill as pickle
import time


def main():
    parser = argparse.ArgumentParser(
        description='''
            This script can be used to train an agent.
            ''',
        epilog='''
            example usage:

            % python train.py test_data/grid.pkl q_learning
            this statement uses as training algorithm q learning and as 
            environment 'test_data/grid.pkl'
            ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'path_instance',
        type=str,
        help='path and filename of the environment object'
    )
    parser.add_argument(
        'learning_method',
        type=str,
        help='''
        learning method which should be used
        
        possible methods: (q_learning)
        '''
    )

    args = parser.parse_args()

    learning_method = args.learning_method

    path_to_file, _ = os.path.split(args.path_instance)

    with open(args.path_instance, 'rb') as f:
        data = pickle.load(f)

    if len(data) == 0:
        raise ImportError('Imported data is empty!')

    start_time = time.time()

    Q = None
    if learning_method == 'q_learning' and \
            data['learning'] == 'q_learning':
        ql_object = QLearning(data)
        Q = ql_object.train()

        for key in Q:
            Q[key] = round(Q[key], 2)

        model = dict(
            learning='q_learning',
            Q=Q,
            width=data['width'],
            height=data['height'],
            actions=data['actions'],
            start_node=data['start_node'],
            terminal_node=data['terminal_node']
        )

        path = os.path.join(path_to_file, 'q_learning.out')

    elif learning_method == 'logical_reasoning' and \
            data['learning'] == 'logical_reasoning':
        lr_object = LogicalReasoning(data)
        KB, final_state = lr_object.train()

        model = dict(
            learning='logical_reasoning',
            KB=KB,
            board=data['board'],
            width=data['width'],
            height=data['height'],
            final_state=final_state,
            start_node=data['start_node'],
            trap_node=data['trap_node'],
            monster_node=data['monster_node']
        )

        path = os.path.join(path_to_file, 'logical_reasoning.out')

    else:
        raise AssertionError('Wrong training type or file!')

    time_for_training = time.time() - start_time

    with open(path, 'wb') as f:
        pickle.dump(model, f)

    print(f'###############################################################\n'
          f'# Utility trained and stored in File "{path}"! \n'
          f'# Time for training: {time_for_training:.3}s\n'
          f'###############################################################')


if __name__ == '__main__':
    main()
