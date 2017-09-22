import numpy as np
import pygame

import config
import utils
from graph import g_graph


class Ant(pygame.sprite.Sprite):
    def __init__(self, atype, aid, pid):
        pygame.sprite.Sprite.__init__(self)
        self.atype = atype
        self.aid = aid
        self.pid_start = pid
        self.pid_prev = -1
        self.pid_next = pid
        self.direction = None
        self.previous_side = 0
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((47, 79, 79))
        self.rect = self.surf.get_rect()
        self.pos = g_graph.nodes_position[self.pid_start]
        self._update_rect(self.pos)
        self.eta = None
        self.eta_left = -0.1
        self.hidden_time = 0.
        self.arrived_pids = [self.pid_prev]
        self.wait = False

    def update(self):
        # if in launch point
        if self.wait:
            return

        print(self.eta_left, self.arrived_pids)
        if self._arrived() and self.pid_next != self.arrived_pids[-1]:
            self.arrived_pids.append(self.pid_next)

            if 'F' in g_graph.i2c[self.pid_next]:
                g_graph.ants_in_F[self.pid_next] = True
                self.wait = True
                return

            for p in np.random.permutation(g_graph.after[self.pid_next]):
                if g_graph.ants_in_F[p] == True:
                    continue
                self.pid_prev = self.pid_next
                self.pid_next = p
                self.pos = g_graph.nodes_position[self.pid_prev]
                self.eta = g_graph.nodes_distance[self.pid_prev, self.pid_next] / self._speed()
                self.eta_left = self.eta
                self.direction = utils.get_direction(g_graph, self.pid_prev, self.pid_next)
                break

        if self.direction is not None:
            interp = self.eta_left / self.eta
            pos_next = g_graph.nodes_position[self.pid_next]
            pos = self.pos[0] * interp + (1 - interp) * pos_next[0], self.pos[1] * interp + (1 - interp) * pos_next[1]
            self.rect.center = utils.lb2lt(pos)
            self.eta_left -= 0.01
            print(self.eta_left)

    def _speed(self):
        if g_graph.flags_main_road[self.pid_prev, self.pid_next]:
            return config.get_int('speed_{}_main'.format(self.atype))
        else:
            return config.get_int('speed_{}_normal'.format(self.atype))

    def _update_rect(self, lbpos):
        ltpos = utils.lb2lt(lbpos)
        self.rect.center = ltpos

    def _arrived(self):
        return self.eta_left < 0

    def __str__(self):
        return '{} {} {}'.format(self.atype, self.aid, self.pid_start)
