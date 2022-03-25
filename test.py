import functools


@functools.total_ordering
class Item:
    def __init__(self, pos, path=None, cost=0):
        if path is None:
            path = []
        self.pos = pos
        self.path = path
        self.cost = cost

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.pos == other.pos

    def __lt__(self, other):
        if not isinstance(other, Item):
            return TypeError
        return self.cost < other.cost

    def __str__(self):
        return 'pos: {}, path: {}, cost: {}'.format(self.pos, self.path, self.cost)


import util

q = util.PriorityQueue()
a = Item((5, 5), ['North', 'South'], 10)
b = Item((5, 5), ['South', 'North'], 5)
c = Item((5, 4), ['East', 'North'], 4)
d = Item((5, 4), ['North', 'East'], 10)
q.update(a, a.cost)
q.update(b, b.cost)
q.update(c, c.cost)
q.update(d, d.cost)
while not q.isEmpty():
    print q.pop()
