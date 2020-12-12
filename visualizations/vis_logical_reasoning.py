"""
Author: Alexander Fichtinger
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def setup_subplots(subplot: plt.subplot, width: int, height: int, color: str, title: str):
    """ Configure subplots.

    :param subplot: plt.subplot
    :param width: int
    :param height: int
    :param color: str
    :param title: str
    """

    subplot.set_xlim(0, width)
    subplot.xaxis.tick_top()
    subplot.set_ylim(height, 0)
    subplot.grid(color=color, linestyle='-', linewidth=1)
    subplot.set_aspect('equal', adjustable='box')
    subplot.set_title(title)


def setup_interface(data: dict):
    """ Setup the whole matplot interface.

    :param data: dict (agent file)
    """

    width = data['width']
    height = data['height']

    start_node = data['start_node']
    gold_node = data['final_state']
    trap_node = data['trap_node']
    monster_node = data['monster_node']
    KB = data['KB']

    # two subplots
    fig, (ax2, ax) = plt.subplots(1, 2)
    fig.set_size_inches(10, 6, forward=True)

    # iterate through grid
    for i in range(height):
        for j in range(width):
            if [i, j] in KB['visited_nodes']:
                ax.add_patch(matplotlib.patches.Rectangle((j, i), 1, 1, color="#c1d9c8"))
            elif [i, j] in KB['avoidance']:
                ax.add_patch(matplotlib.patches.Rectangle((j, i), 1, 1, color="#e86b6b"))
            else:
                ax.add_patch(matplotlib.patches.Rectangle((j, i), 1, 1, color="#ededed"))

    # set text in the visualized board
    ax.text(start_node[1] + 0.5, start_node[0] + 0.5,
            'Start',
            horizontalalignment='center', verticalalignment='center',
            color='#383838', size=9)

    ax.text(gold_node[1] + 0.5, gold_node[0] + 0.5,
            'Goal',
            horizontalalignment='center', verticalalignment='center',
            color='white', size=9)

    # set text in the real board
    ax2.text(start_node[1] + 0.5, start_node[0] + 0.5,
             'Start',
             horizontalalignment='center', verticalalignment='center',
             color='#383838', size=9)

    ax2.text(gold_node[1] + 0.5, gold_node[0] + 0.5,
            'Goal',
            horizontalalignment='center', verticalalignment='center',
            color='white', size=9)

    ax2.text(trap_node[1] + 0.5, trap_node[0] + 0.5,
            'Trap',
            horizontalalignment='center', verticalalignment='center',
            color='white', size=8)

    ax2.text(monster_node[1] + 0.5, monster_node[0] + 0.5,
            'Monster',
            horizontalalignment='center', verticalalignment='center',
            color='white', size=7)

    # draw background in specific states
    ax.add_patch(matplotlib.patches.Rectangle((start_node[1], start_node[0]), 1, 1, color="white"))
    ax.add_patch(matplotlib.patches.Rectangle((gold_node[1], gold_node[0]), 1, 1, color="#2ab456"))

    ax2.add_patch(matplotlib.patches.Rectangle((trap_node[1], trap_node[0]), 1, 1, color="#d14141"))
    ax2.add_patch(matplotlib.patches.Rectangle((monster_node[1], monster_node[0]), 1, 1, color="#d14141"))
    ax2.add_patch(matplotlib.patches.Rectangle((gold_node[1], gold_node[0]), 1, 1, color="#2ab456"))

    # set suplot settings
    setup_subplots(ax, width, height, 'white', 'Logical Results of AI')
    setup_subplots(ax2, width, height, 'darkgray', 'Real Game Board')
