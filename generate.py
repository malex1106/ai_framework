"""
Author: Alexander Fichtinger
"""

from generation_instance.grid_generator import Grid
import argparse
import os
import dill as pickle


def main():
    parser = argparse.ArgumentParser(
        description='''
        This script can be used to generate a WIDTHxHEIGHT grid.
        Terminal nodes will be taken randomly.
        The resulting file can be used for the reinforcement learning algorithm.
        ''',
        epilog='''
        example usage:

        % python generate.py 5 6 test_data/grid.pkl
        this statement generates a 5x6 grid and writes it into
        the pickle file 'test_data/grid.pkl'
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'grid_width',
        type=int,
        help='width of the grid (>= 3)'
    )
    parser.add_argument(
        'grid_height',
        type=int,
        help='width of the grid (>= 3)'
    )
    parser.add_argument(
        'path_instance',
        type=str,
        help='path and filename of the created object'
    )

    args = parser.parse_args()

    grid_object = Grid(width=args.grid_width, height=args.grid_height)

    width = grid_object.width
    height = grid_object.height

    gamma = grid_object.gamma
    grid = grid_object.grid
    start_node = grid_object.start_node
    terminal_node = grid_object.terminal_node
    actions = grid_object.default_actions
    rewards = grid_object.rewards

    path_to_file, filename = os.path.split(args.path_instance)
    if path_to_file != '':
        os.makedirs(path_to_file, exist_ok=True)

    grid_environment = dict(width=width,
                            height=height,
                            gamma=gamma,
                            grid=grid,
                            start_node=start_node,
                            terminal_node=terminal_node,
                            actions=actions,
                            rewards=rewards
                            )

    with open(args.path_instance, 'wb') as f:
        pickle.dump(grid_environment, f)

    print(f'#######################################\n'
          f'# Environment "{args.path_instance}" created! \n'
          f'#######################################')


if __name__ == '__main__':
    main()
