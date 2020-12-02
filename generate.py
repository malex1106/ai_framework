"""
Author: Alexander Fichtinger
"""

from generation_instance.grid_generator import Grid
from generation_instance.game_board_generator import GameBoard
import argparse
import os
import dill as pickle


def main():
    parser = argparse.ArgumentParser(
        description='''
        This script can be used to generate a WIDTHxHEIGHT environment.
        The resulting file either can be used for q-learning or logical reasioning.
        ''',
        epilog='''
        example usage:

        % python generate.py 5 6 test_data/grid.pkl grid
        This statement generates a 5x6 grid and writes it into
        the pickle file 'test_data/grid.pkl'. It can be used for
        q-learning.
        
        % python generate.py 5 6 test_data/board.pkl board
        This statement generates a 5x6 board and writes it into
        the pickle file 'test_data/board.pkl'. It can be used for
        logical reasioning.
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'width',
        type=int,
        help='width of the grid/board (>= 3)'
    )
    parser.add_argument(
        'height',
        type=int,
        help='width of the grid/board (>= 3)'
    )
    parser.add_argument(
        'path_instance',
        type=str,
        help='path and filename of the created object'
    )
    parser.add_argument(
        'type',
        type=str,
        help='type of environment'
    )

    args = parser.parse_args()

    if args.type == 'grid':
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
    elif args.type == 'board':
        board_object = GameBoard(width=args.width, height=args.height)

        width = board_object.width
        height = board_object.height

        board = board_object.board
        start_node = board_object.start_node
        draft_nodes = board_object.draft_nodes
        stengh_nodes = board_object.stengh_nodes

        default_states = board_object.default_states
        default_senses = board_object.default_senses

        environment = dict(learning='logical_reasioning',
                           width=width,
                           height=height,
                           board=board,
                           start_node=start_node,
                           draft_nodes=draft_nodes,
                           stengh_nodes=stengh_nodes,
                           default_states=default_states,
                           default_senses=default_senses
                           )
    else:
        raise AssertionError('Type not found!')

    path_to_file, filename = os.path.split(args.path_instance)
    if path_to_file != '':
        os.makedirs(path_to_file, exist_ok=True)

    with open(args.path_instance, 'wb') as f:
        pickle.dump(environment, f)

    print(f'#######################################\n'
          f'# Environment "{args.path_instance}" created! \n'
          f'#######################################')


if __name__ == '__main__':
    main()
