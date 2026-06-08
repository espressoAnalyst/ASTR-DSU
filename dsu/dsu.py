from collections import defaultdict

class StringDSU:
    """Disjoint Set Union implementation for string-based identifiers."""
    
    def __init__(self):
        self.parent = {}
        self.size = {}

    def _initialize_node(self, node: str) -> None:
        """Lazy initialization for new elements."""
        if node not in self.parent:
            self.parent[node] = node
            self.size[node] = 1

    def find(self, node: str) -> str:
        """Finds the root representative of a node with path compression."""
        self._initialize_node(node)
        
        # Path compression: point node directly to the root
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
            
        return self.parent[node]

    def union(self, node1: str, node2: str) -> bool:
        """Merges two sets using union by size. Returns True if a merge occurred."""
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 == root2:
            return False

        # Union by size: attach the smaller tree to the larger tree
        if self.size[root1] < self.size[root2]:
            root1, root2 = root2, root1

        self.parent[root2] = root1
        self.size[root1] += self.size[root2]
        return True

    def get_grouped_components(self) -> dict:
        """Aggregates and returns all disjoint sets."""
        groups = defaultdict(list)
        for node in self.parent.keys():
            root = self.find(node)
            groups[root].append(node)
        return dict(groups)