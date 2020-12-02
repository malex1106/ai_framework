"""
Author: Alexander Fichtinger
"""

import matplotlib.pyplot as plt
import dill as pickle
import argparse
from visualizations import vis_q_learning


def main():
    parser = argparse.ArgumentParser(
        description='''
                This script can be used to visualize the outcome files from training.
                ''',
        epilog='''
                example usage:

                % python view.py test_data/grid.pkl
                this statement will show a visual representation of the file
                 'test_data/q_learning.outcome'
                ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'path_instance',
        type=str,
        help='path and filename of the outcome object/agent'
    )

    args = parser.parse_args()

    with open(args.path_instance, 'rb') as f:
        data = pickle.load(f)

    if data['learning'] == 'q_learning':
        vis_q_learning.setup_interface(data)

    plt.show()


if __name__ == '__main__':
    main()
