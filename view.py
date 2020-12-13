"""
Author: Alexander Fichtinger
"""

import matplotlib.pyplot as plt
import dill as pickle
import argparse

from visualizations import vis_q_learning
from visualizations import  vis_logical_reasoning
from visualizations import vis_decision_tree


def main():
    parser = argparse.ArgumentParser(
        description='''
                This script can be used to visualize the outcome files from training.
                ''',
        epilog='''
                example usage:

                % python view.py test_data/q_learning.out
                this statement will show a visual representation of the file
                 'test_data/q_learning.out'
                 
                % python view.py test_data/logical_reasoning.out
                this statement will show a visual representation of the file
                 'test_data/logical_reasoning.out'
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
    elif data['learning'] == 'logical_reasoning':
        vis_logical_reasoning.setup_interface(data)
    elif data['learning'] == 'id3':
        vis_decision_tree.setup_interface(data)

    plt.show()


if __name__ == '__main__':
    main()
