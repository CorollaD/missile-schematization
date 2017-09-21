from ant import Ant
from graph import g_graph


class Colony():
    def __init__(self):
        self.dict_ant_num = {'A': 6, 'B': 6, 'C': 12}
        self.ants = []

        # init ants
        for node in ('D1', 'D2'):
            position = g_graph.c2i[node]
            for key, value in self.dict_ant_num.items():
                for i in range(value // 2):
                    i_ant = Ant(key, 0, position)
                    self.ants.append(i_ant)
        for i, ant in enumerate(self.ants):
            ant._id = i
            print(ant)
