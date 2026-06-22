import numpy as np

class GlobalArrayDSU:
    def __init__(self, N: int):
        """
        Initializes the DSU with an exact starting size N.
        """
        self.N = N
        
        # Standard RAM initialization
        self.parent = np.arange(self.N, dtype=np.int32)
        self.size = np.ones(self.N, dtype=np.int32)
        
        # Hashmap to track Embedding IDs (strings/hashes) to Array Indices (integers)
        self.embedding_hashmap = {}

    def resize_and_duplicate(self, new_N: int):
        """
        Resizes the arrays and duplicates the old data into the beginning.
        """
        if new_N <= self.N:
            return

        print(f"   [*] Resizing and Duplicating Global Arrays from {self.N} to {new_N}...")
        
        # 1. Allocate new standard arrays
        new_parent = np.arange(new_N, dtype=np.int32)
        new_size = np.ones(new_N, dtype=np.int32)
        
        # 2. Duplicate old memory block into the new arrays
        new_parent[:self.N] = self.parent
        new_size[:self.N] = self.size
        
        # 3. Swap pointers
        self.parent = new_parent
        self.size = new_size
        self.N = new_N

    def process_edge_list(self, edges: np.ndarray):
        """
        Ingests edges. Designed to accept a binary-loaded 2D NumPy array (shape: [E, 2]).
        """
        if len(edges) == 0:
            return
            
        # Iterate over the binary array rows
        for u, v in edges:
            self._union(int(u), int(v))

    def find(self, i: int) -> int:
        """Finds the absolute root of node i with Two-Pass Path Compression."""
        if i >= self.N:
            return -1 
            
        root = i
        while root != self.parent[root]:
            root = self.parent[root]
            
        curr = i
        while curr != root:
            curr, self.parent[curr] = self.parent[curr], root
            
        return root

    def _union(self, u: int, v: int) -> bool:
        """Merges two components using Union by Size."""
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            return False

        # Guaranteed swap logic
        if self.size[root_u] < self.size[root_v]:
            root_u, root_v = root_v, root_u

        self.parent[root_v] = root_u
        self.size[root_u] += self.size[root_v]
        return True