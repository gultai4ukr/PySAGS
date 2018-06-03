from collections import deque


class Connection(object):

    def __init__(self, obj_from, obj_to, key_from=None, key_to=None):
        self.obj_from = obj_from
        self.obj_to = obj_to
        self.key_from = key_from
        self.key_to = key_to
        self.data = 0

    def send(self):
        self.obj_to.receive(self.data, self.key_to)

    def receive(self, data):
        self.data = data
        self.send()


class AbstractNode(object):

    def __init__(self):
        self.data = {}
        self.connections = {}

    def add_connection(self, conn, key):
        self.connections[key] = conn

    def send(self):
        for key, conn in self.connections.items():
            conn.receive(self.data.get(key, 0), key)

    def receive(self, data, key):
        self.data[key] = data

    def process(self):
        raise NotImplementedError


class DataStream(object):

    def __init__(self, data, key):
        # todo: add possibility to specify fp/path to file with data
        self.queue = deque(data)
        self.key = key
        self.connection = None

    def add_connection(self, conn):
        self.connection = conn

    def send(self):
        self.connection.receive(self.queue.popleft() if len(self.queue) else 0)


class SystolicArray(object):

    def __init__(self, size, nodes_by_class, input_streams, connections):
        self.current_step = 0
        self.n, self.m = size
        self.array = [[None] * self.m for _ in range(self.n)]
        for node_cls, positions in nodes_by_class:
            for rows, cols in positions:
                for r in self.fix_sequence_of_indexes(rows):
                    for c in self.fix_sequence_of_indexes(cols):
                        self.array[r][c] = node_cls()
        for i in range(self.n):
            assert None not in self.array[i]
        self.input_streams = input_streams
        for objs_from, objs_to, key_from, key_to in connections:
            objs_from = self.get_elements_sequence(objs_from)
            objs_to = self.get_elements_sequence(objs_to)
            assert len(objs_from) == len(objs_to)
            for obj_from, objs_to in zip(objs_from, objs_to):
                conn = Connection(obj_from, objs_to, key_from, key_to)
                obj_from.add_connection(conn)

    @staticmethod
    def fix_sequence_of_indexes(seq):
        if isinstance(seq, int):
            seq = [seq]
        assert isinstance(seq, (range, list))
        return seq

    def get_nodes_by_indexes(self, rows, cols):
        assert isinstance(rows, int) or isinstance(cols, int), \
            "Now this function doesn't support 2D arrays"  # todo: deal with it
        rows = self.fix_sequence_of_indexes(rows)
        cols = self.fix_sequence_of_indexes(cols)
        objs = []
        for r in rows:
            for c in cols:
                objs.append(self.array[r][c])
        return objs

    def get_elements_sequence(self, seq):
        # elements == nodes + data streams
        if isinstance(seq, tuple):
            assert len(seq) == 2
            return self.get_nodes_by_indexes(*seq)
        if isinstance(seq, DataStream):
            return [seq]
        assert isinstance(seq, list)
        return seq

    def iterate(self, n_times=1):
        for _ in range(n_times):
            for streams in self.input_streams:
                if isinstance(streams, DataStream):
                    streams = [streams]
                assert isinstance(streams, list)
                for stream in streams:
                    stream.send()
            for r in range(self.n):
                for c in range(self.m):
                    self.array[r][c].send()
                    self.array[r][c].process()
