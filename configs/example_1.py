from base import AbstractNode, DataStream


class Node(AbstractNode):

    def process(self):
        self.data['c'] += self.data['a'] * self.data['b']


ARRAY_SIZE = (1, 3)
NODES_BY_CLASS = {
    Node: [(0, range(0, 3))],
}
INPUT_STREAMS = {
    'a': DataStream([], 'a'),
    'b': [DataStream([], 'b')] * 3,
}
CONNECTIONS = [
    (INPUT_STREAMS['a'], (0, 0), 'a', 'a'),
    ((0, range(0, 2)), (0, range(1, 3)), 'a', 'a'),
    (INPUT_STREAMS['b'], (0, range(0, 3)), 'b', 'b'),
    ((0, 2), (0, 2), 'a', 'c'),
    ((0, range(2, 0, -1)), (0, range(1, -1, -1)), 'c', 'c'),
]
