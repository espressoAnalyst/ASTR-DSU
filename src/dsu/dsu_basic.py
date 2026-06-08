class DSU:

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, node):

        if node not in self.parent:
            self.parent[node] = node
            self.rank[node] = 0

    def find(self, node):

        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])

        return self.parent[node]

    def union(self, u, v):

        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            return

        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v

        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u

        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1

    def get_components(self):

        components = {}

        for node in self.parent:

            root = self.find(node)

            if root not in components:
                components[root] = []

            components[root].append(node)

        return components