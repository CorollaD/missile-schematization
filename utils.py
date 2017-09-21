import numpy as np


def lb2lt(pos):
    return np.uint16(4 * pos[0]), np.uint16(650 - 4 * pos[1] - 25)

def get_color(name='BLACK'):
    if name == 'RED':
        return (255, 0, 0)
    elif name == 'GREEN':
        return [0, 255, 0]
    elif name == 'BLUE':
        return [0, 0, 255]
    elif name == 'WHITE':
        return [255, 255, 255]
    else:
        return [0, 0, 0]

def get_direction(graph, pid1, pid2):
    pos1 = graph.nodes_position[pid1]
    pos2 = graph.nodes_position[pid2]
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    norm = np.linalg.norm((dx, dy))
    return dx / norm, dy / norm
