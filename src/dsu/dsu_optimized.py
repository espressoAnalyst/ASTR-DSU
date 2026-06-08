import numpy as np


class OptimizedDSU:

    def __init__(self, max_nodes):

        # Parent array
        self.parent = np.arange(max_nodes, dtype=np.int32)

        # Rank array
        self.rank = np.zeros(max_nodes, dtype=np.int8)

    def find(self, node):

        while self.parent[node] != node:

            # Path compression
            self.parent[node] = self.parent[self.parent[node]]

            node = self.parent[node]

        return node

    def union(self, u, v):

        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            return

        # Union by rank
        if self.rank[root_u] < self.rank[root_v]:

            self.parent[root_u] = root_v

        elif self.rank[root_u] > self.rank[root_v]:

            self.parent[root_v] = root_u

        else:

            self.parent[root_v] = root_u

            self.rank[root_u] += 1

    def get_components(self):

        components = {}

        for node in range(len(self.parent)):

            root = self.find(node)

            if root not in components:
                components[root] = []

            components[root].append(node)

        return components