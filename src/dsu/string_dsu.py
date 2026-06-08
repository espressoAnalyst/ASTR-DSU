class StringDSU:

    def __init__(self):
        self.parent = {}
        self.size = {}

    def make_set(self, x):

        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1

    def find(self, x):

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, a, b):

        self.make_set(a)
        self.make_set(b)

        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return

        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]

    def get_components(self):

        components = {}

        for node in self.parent:

            root = self.find(node)

            if root not in components:
                components[root] = []

            components[root].append(node)

        return components