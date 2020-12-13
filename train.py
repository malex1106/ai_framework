"""
Author: Alexander Fichtinger
"""

from reinforcement_learning.q_learning import QLearning
from reinforcement_learning.logical_reasoning import LogicalReasoning
from decision_trees.id3 import DecisionTree, TreeNode

import numpy as np
import argparse
import os
import dill as pickle
import json
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
            
            % python train.py test_data/board.pkl logical_reasoning
            this statement uses logical reasoning and as 
            environment 'test_data/board.pkl'
            
            % python train.py test_data/data.json id3
            this statement uses as training algorithm id3 and as 
            data 'test_data/data.json'
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
        learning method which should be used,
        
        possible methods: (q_learning, logical_reasoning, id3)
        '''
    )

    args = parser.parse_args()

    learning_method = args.learning_method

    path_to_file, _ = os.path.split(args.path_instance)

    if learning_method == 'q_learning' or learning_method == 'logical_reasoning':
        with open(args.path_instance, 'rb') as f:
            data = pickle.load(f)
    elif learning_method == 'id3':
        with open(args.path_instance, 'r') as f:
            data = json.load(f)

    if len(data) == 0:
        raise ImportError('Imported data is empty!')

    start_time = time.time()

    if learning_method == 'q_learning' and \
            data['learning'] == 'q_learning':
        Q = None
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
    elif learning_method == 'id3' and \
            data['learning'] == 'id3':
        data_list = data['data']
        data_array = np.asarray(data_list)
        tree_object = DecisionTree()
        root_node = tree_object.split_data(data_array)

        print(f'###############################################################\n'
              f'# The tree looks like: \n# {root_node}')

        model = dict(learning='id3',
                     data=data['data'],
                     root_node=root_node
                     )

        path = os.path.join(path_to_file, 'id3.out')
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
