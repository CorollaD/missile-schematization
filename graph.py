import numpy as np
import pandas as pd
import pygame
from pygame import draw
import pygame.gfxdraw as xdraw

import utils
from biqueue import BiQueue


class Graph():

    def __init__(self):
        self.pnum = {'A': 130, 'D': 2, 'Z': 6, 'F': 60, 'J': 62}
        self.n_all = 130
        self.n_d = 2
        self.n_z = 6
        self.n_f = 60
        self.n_j = 62

        self.c2i = {}
        self.i2c = {}
        self.after = {}
        self.nodes_position = np.zeros([self.n_all, 2], dtype=np.float16)
        self.nodes_distance = np.zeros([self.n_all, self.n_all], dtype=np.float16)
        self.flags_main_road = np.zeros([self.n_all, self.n_all], dtype=np.bool)
        self.ants_on_normal_road = np.zeros([self.n_all, self.n_all], dtype=BiQueue)
        self.ants_on_main_road = np.zeros([self.n_all, self.n_all, 2], dtype=BiQueue)
        self.ants_in_reload = np.zeros([self.n_all], dtype=BiQueue)
        self.ants_in_F = np.zeros([self.n_all], dtype=np.bool)

        # init road state
        for i in range(self.n_all):
            for j in range(self.n_all):
                self.ants_on_normal_road[i, j] = BiQueue()
                for k in (0, 1):
                    self.ants_on_main_road[i, j, k] = BiQueue()
            self.ants_in_reload[i] = BiQueue()

        # init
        self._read_data()

    def _distance(self, pid1, pid2):
        dx = self.nodes_position[pid1, 0] - self.nodes_position[pid2, 0]
        dy = self.nodes_position[pid1, 1] - self.nodes_position[pid2, 1]
        return np.linalg.norm((dx, dy), 2)

    def _read_data(self):
        file = 'missile-graph.xls'

        ## read pos
        df = pd.read_excel(file, sheetname=0)
        df = df[df.type == df.type] # get rid of 'NaN'

        # init attr and pos mat
        for i in range(len(df)):
            itype = df.iloc[i][0]
            self.c2i[itype] = i
            self.i2c[i] = itype
            self.nodes_position[i, 0] = df.iloc[i][1]
            self.nodes_position[i, 1] = df.iloc[i][2]

        ## read edges
        # init distance
        for i in range(self.pnum['A']):
            for j in range(self.pnum['A']):
                self.nodes_distance[i, j] = float('inf')
            self.after[i] = []

        df = pd.read_excel(file, sheetname=1)

        for i in range(len(df)):
            end1 = df.iloc[i][0]
            end2 = df.iloc[i][1]
            #print(end1, end2)
            pid1 = self.c2i[end1]
            pid2 = self.c2i[end2]
            euc_dist = self._distance(pid1, pid2)
            # if mind > euc_dist:
            #     mind = euc_dist
            # print(pid1, pid2, euc_dist, mind)

            # calc dist
            self.nodes_distance[pid1, pid2] = euc_dist
            self.nodes_distance[pid2, pid1] = euc_dist

            # calc alter
            self.after[pid1].append(pid2)
            self.after[pid2].append(pid1)

        # debug self.after
        for i in range(self.pnum['A']):
            tmp = [self.i2c[x] for x in self.after[i]]
            # print(self.i2c[i], tmp)

        ## read main roads
        df = pd.read_excel(file, sheetname=2)
        for i in range(len(df)):
            end1 = df.iloc[i][0]
            end2 = df.iloc[i][1]
            pid1 = self.c2i[end1]
            pid2 = self.c2i[end2]
            self.flags_main_road[pid1, pid2] = True
            self.flags_main_road[pid2, pid1] = True

    def draw(self, screen):
        # draw roads
        for i in range(self.n_all):
            for j in range(i, self.n_all):
                if not self.nodes_distance[i, j] < float('inf'):
                    continue

                pos_i = utils.lb2lt(tuple(self.nodes_position[i]))
                pos_j = utils.lb2lt(tuple(self.nodes_position[j]))
                color = utils.get_color()
                size = 2
                if self.flags_main_road[i, j]:
                    color = utils.get_color('RED')
                    size = 3
                draw.aaline(screen, color, pos_i, pos_j)
        # draw nodes
        for i in range(self.n_all):
            pos = utils.lb2lt(tuple(self.nodes_position[i]))
            if 'D' in self.i2c[i]:
                xdraw.filled_circle(screen, pos[0], pos[1], 8, utils.get_color('RED'))
            elif 'Z' in self.i2c[i]:
                xdraw.filled_circle(screen, pos[0], pos[1], 6, utils.get_color('BLUE'))
            elif 'J' in self.i2c[i]:
                xdraw.filled_circle(screen, pos[0], pos[1], 4, utils.get_color('BLACK'))
            elif 'F' in self.i2c[i]:
                xdraw.box(screen, (pos[0] - 4, pos[1] - 4, 8, 8), (139, 19, 69))


g_graph = Graph()
