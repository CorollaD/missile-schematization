import numpy as np


class BiQueue():

    def __init__(self):
        self.data = []

    def append(self, x):
        self.data.append(x)

    def appendleft(self, x):
        self.data.insert(0, x)

    def pop(self):
        self.data = self.data[:-1]

    def popleft(self):
        self.data = self.data[1:]

    def remove(self, x):
        try:
            self.data.remove(x)
        except:
            pass

    def front(self):
        return self.data[0]

    def back(self):
        return self.data[-1]

    def qsize(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)


if __name__ == '__main__':
    a = np.zeros([2, 3], dtype=BiQueue)
    que = BiQueue()
    que.append('c')
    que.append('e')
    que.appendleft('a')
    a[0, 1] = que

    c = a[0, 2]
    print(c.qsize())
