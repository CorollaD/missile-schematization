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

            if 'F' in g_graph.i2c[self.pid_next]:
                self.wait = True
                return

            self.arrived_pids.append(self.pid_next)
            for p in np.random.permutation(g_graph.after[self.pid_next]):

                if 'F' in g_graph.i2c[p] and not g_graph.ants_in_F[p] and \
                                g_graph.ants_on_normal_road[self.pid_prev, p].qsize() < 1:
                    self.pid_prev = self.pid_next
                    self.pid_next = p
                    self.pos = g_graph.nodes_position[self.pid_prev]
                    self.eta = g_graph.nodes_distance[self.pid_prev, self.pid_next] / self._speed('normal')
                    self.eta_left = self.eta
                    self.direction = utils.get_direction(g_graph, self.pid_prev, self.pid_next)
                    g_graph.ants_in_F[p] = True
                    g_graph.ants_on_normal_road[self.pid_prev, self.pid_next].append(self)
                    break

                # print(globals.g_graph.i2c[self.pid_next], globals.g_graph.i2c[p])
                if g_graph.flags_main_road[self.pid_prev, self.pid_next]:
                    g_graph.ants_on_main_road[self.pid_prev, self.pid_next, self.previous_side].remove(self)
                    anti_ants0 = g_graph.ants_on_main_road[self.pid_next, self.pid_prev, 0]
                    anti_ants1 = g_graph.ants_on_main_road[self.pid_next, self.pid_prev, 1]
                    # if both ways are blocked, wait
                    if anti_ants0.qsize() > 0 and anti_ants1.qsize() > 0:
                        continue
                    # if either is clear
                    self.pid_prev = self.pid_next
                    self.pid_next = p
                    self.pos = g_graph.nodes_position[self.pid_prev]
                    self.eta = g_graph.nodes_distance[self.pid_prev, self.pid_next] / self._speed('main')
                    self.eta_left = self.eta
                    self.direction = utils.get_direction(g_graph, self.pid_prev, self.pid_next)
                    if anti_ants0.qsize() > 0:
                        self.previous_side = 0
                        g_graph.ants_on_main_road[self.pid_prev, self.pid_next, 1].append(self)
                    else:
                        self.previous_side = 1
                        g_graph.ants_on_main_road[self.pid_prev, self.pid_next, 0].append(self)
                    break
                else:
                    g_graph.ants_on_normal_road[self.pid_prev, self.pid_next].remove(self)
                    anti_ants = g_graph.ants_on_normal_road[self.pid_next, self.pid_prev]
                    if anti_ants.qsize() > 0:
                        continue
                    else:
                        self.pid_prev = self.pid_next
                        self.pid_next = p
                        self.pos = g_graph.nodes_position[self.pid_prev]
                        self.eta = g_graph.nodes_distance[self.pid_prev, self.pid_next] / self._speed('normal')
                        self.eta_left = self.eta
                        self.direction = utils.get_direction(g_graph, self.pid_prev, self.pid_next)
                        g_graph.ants_on_normal_road[self.pid_prev, self.pid_next].append(self)
                        break

        if self.direction is not None:
            interp = self.eta_left / self.eta
            pos_next = g_graph.nodes_position[self.pid_next]
            pos = self.pos[0] * interp + (1 - interp) * pos_next[0], self.pos[1] * interp + (1 - interp) * pos_next[1]
            self.rect.center = utils.lb2lt(pos)
            self.eta_left -= 0.01
            print(self.eta_left)

    def _speed(self, rtype):
        if rtype == 'main':
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
