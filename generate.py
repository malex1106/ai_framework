"""
Author: Alexander Fichtinger
"""

from generation_instance.grid_generator import Grid
from generation_instance.game_board_generator import GameBoard
from generation_instance.data_generation import TestData

import argparse
import os
import dill as pickle
import json


def main():
    parser = argparse.ArgumentParser(
        description='''
        This script can be used for creating an environment or data samples.
        The resulting file either can be used for q-learning, logical reasioning or id3.
        ''',
        epilog='''
        example usage:

        % python generate.py grid test_data/grid.pkl -width 5 -height 6
        This statement generates a 5x6 grid and writes it into
        the pickle file 'test_data/grid.pkl'. It can be used for
        q-learning.
        
        % python generate.py board test_data/board.json -width 5 -height 5
        This statement generates a 5x5 board and writes it into
        the pickle file 'test_data/board.pkl'. It can be used for
        logical reasioning.
        
        % python generate.py data test_data/data.json -features 5 -samples 5
        This statement creates random data and writes it into 
        the json file 'test_data/data.json'. It can be used for 
        creating decision trees.
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'type',
        type=str,
        help='type of environment'
    )
    parser.add_argument(
        '-width',
        type=int,
        required=False,
        default=5,
        help='width of the grid/board (for grid: >=3, for board: >=5)'
    )
    parser.add_argument(
        '-height',
        type=int,
        required=False,
        default=5,
        help='width of the grid/board (for grid: >=3, for board: >=5)'
    )
    parser.add_argument(
        '-features',
        type=int,
        required=False,
        default=2,
        help='features for the data generation'
    )
    parser.add_argument(
        '-samples',
        type=int,
        required=False,
        default=6,
        help='sample size for the data generation'
    )
    parser.add_argument(
        'path_instance',
        type=str,
        help='path and filename of the created object'
    )

    args = parser.parse_args()

    # check path
    path_to_file, filename = os.path.split(args.path_instance)
    if path_to_file != '':
        os.makedirs(path_to_file, exist_ok=True)

    # check type
    if args.type == 'grid':
        if args.width < 3 or args.height < 3:
            raise ValueError('Width and height should be greater-equal 3!')

        grid_object = Grid(width=args.width, height=args.height)

        width = grid_object.width
        height = grid_object.height

        gamma = grid_object.gamma
        grid = grid_object.grid
        start_node = grid_object.start_node
        terminal_node = grid_object.terminal_node
        actions = grid_object.default_actions
        rewards = grid_object.rewards

        environment = dict(learning='q_learning',
                           width=width,
                           height=height,
                           gamma=gamma,
                           grid=grid,
                           start_node=start_node,
                           terminal_node=terminal_node,
                           actions=actions,
                           rewards=rewards
                           )

        with open(args.path_instance, 'wb') as f:
            pickle.dump(environment, f)

    elif args.type == 'board':
        if args.width < 5 or args.height < 5:
            raise ValueError('Width and height should be greater-equal 5!')

        board_object = GameBoard(width=args.width, height=args.height)

        width = board_object.width
        height = board_object.height

        board = board_object.board
        start_node = board_object.start_node
        draft_nodes = board_object.draft_nodes
        stench_nodes = board_object.stench_nodes

        trap_node = board_object.trap_node
        monster_node = board_object.monster_node
        goal_node = board_object.goal_node

        default_states = board_object.default_states
        default_senses = board_object.default_senses

        environment = dict(learning='logical_reasoning',
                           width=width,
                           height=height,
                           board=board,
                           start_node=start_node,
                           draft_nodes=draft_nodes,
                           stench_nodes=stench_nodes,
                           trap_node=trap_node,
                           monster_node=monster_node,
                           goal_node=goal_node,
                           default_states=default_states,
                           default_senses=default_senses
                           )

        with open(args.path_instance, 'wb') as f:
            pickle.dump(environment, f)

    elif args.type == 'data':
        data_object = TestData(feature_size=args.features, sample_size=args.samples)
        data_list = data_object.data_array.tolist()
        test_data = dict(learning='id3',
                         data=data_list
                         )

        with open(args.path_instance, 'w') as f:
            json.dump(test_data, f)
    else:
        raise AssertionError('Type not found!')

    print(f'#######################################\n'
          f'# File "{args.path_instance}" created! \n'
          f'#######################################')


if __name__ == '__main__':
    main()
