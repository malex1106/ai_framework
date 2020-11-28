import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import dill as pickle
import argparse


def setup_subplots(subplot: plt.subplot, width: int, height: int, color: str, title: str):
    subplot.set_xlim(0, width)
    subplot.xaxis.tick_top()
    subplot.set_ylim(height, 0)
    subplot.grid(color=color, linestyle='-', linewidth=1)
    subplot.set_aspect('equal', adjustable='box')
    subplot.set_title(title)


def check_color(best: int) -> str:
    if 99 <= best <= 100:
        color = '#0a1924'
    elif 80 <= best < 99:
        color = '#172f40'
    elif 60 <= best < 80:
        color = '#30546e'
    elif 40 <= best < 60:
        color = '#517d9c'
    elif 20 <= best < 40:
        color = '#76a3c2'
    else:
        color = '#9ac0db'

    return color


def show_policy(best_action: str):
    dx, dy = 0, 0

    if best_action == 'down':
        dx = 0
        dy = 1 - 0.2
    elif best_action == 'up':
        dx = 0
        dy = -1 + 0.2
    elif best_action == 'right':
        dx = 1 - 0.2
        dy = 0
    elif best_action == 'left':
        dx = -1 + 0.2
        dy = 0

    return dx, dy


def main():
    parser = argparse.ArgumentParser(
        description='''
                This script can be used to visualize the outcome files from training.
                ''',
        epilog='''
                example usage:

                % python view.py test/grid.pkl
                this statement will show a visual representation of the file
                 'test/q_learning.outcome'
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

    width = data['width']
    height = data['height']

    start_node = data['start_node']
    terminal_node = data['terminal_node']
    actions = data['actions']
    Q = data['Q']

    fig, (ax, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(10, 6, forward=True)

    for i in range(height):
        for j in range(width):
            best, best_action = 0, ''

            for act in actions:
                if Q[(i, j, act)] > best:
                    best = Q[(i, j, act)]
                    best_action = act

            color = check_color(best)

            ax.add_patch(matplotlib.patches.Rectangle((j, i), 1, 1, color=color))

            dx, dy = show_policy(best_action)

            if i != terminal_node[0] or j != terminal_node[1]:
                ax.text(j + 0.5, i + 0.5,
                        str(best),
                        horizontalalignment='center', verticalalignment='center',
                        color='white', size=9)
                ax2.add_patch(matplotlib.patches.Arrow(j + 0.5, i + 0.5, dx, dy, width=0.1, color='black'))

    ax.add_patch(matplotlib.patches.Rectangle((start_node[1], start_node[0]), 1, 1, color="white"))
    ax.add_patch(matplotlib.patches.Rectangle((terminal_node[1], terminal_node[0]), 1, 1, color="#32a852"))

    setup_subplots(ax, width, height, 'white', 'Value Function')
    setup_subplots(ax2, width, height, '#1a1a1a', 'Utility Function')

    plt.show()


if __name__ == '__main__':
    main()
