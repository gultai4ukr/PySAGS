from base import AbstractNode, DataStream


class Node(AbstractNode):

    def process(self):
        self.data['c'] += self.data['a'] * self.data['b']


ARRAY_SIZE = (1, 3)
KEYS = ['a', 'b', 'c']
NODES_BY_CLASS = {
    Node: [(0, range(0, 3))],
}
INPUT_STREAMS = {
    'a': DataStream([1, 0, 2, 0, 3, 0, 4], 'a'),
    'b': [
        DataStream([0, 0, 0, 0, 3, 0, 3], 'b'),
        DataStream([0, 0, 0, 2, 0, 2], 'b'),
        DataStream([0, 0, 1, 0, 1], 'b'),
    ],
    'c': DataStream([0, 0, 0, 0, 0], 'c'),
}
CONNECTIONS = [
    (INPUT_STREAMS['a'], (0, 0), 'a', 'a'),
    ((0, range(0, 2)), (0, range(1, 3)), 'a', 'a'),
    (INPUT_STREAMS['b'], (0, range(0, 3)), 'b', 'b'),
    (INPUT_STREAMS['c'], (0, 2), 'c', 'c'),
    ((0, range(2, 0, -1)), (0, range(1, -1, -1)), 'c', 'c'),
]
