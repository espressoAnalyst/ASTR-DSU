import os
import numpy as np

class GlobalArrayDSU:
    def __init__(self, N: int, parent_path: str, size_path: str):
        """
        Initializes the DSU by memory-mapping arrays directly from disk.
        Safely handles pre-created 0-byte (empty) array files.
        """
        self.N = N
        self.parent_path = parent_path
        self.size_path = size_path

        # Helper to check if array files exist AND have actual data in it
        def is_valid_file(filepath):
            return os.path.exists(filepath) and os.path.getsize(filepath) > 0

        # 2. Scenario A: Array files exist AND have data -> Load via memmap
        if is_valid_file(parent_path) and is_valid_file(size_path):
            # 1. Load the old arrays in read-only mode to check their size
            old_parent = np.load(parent_path, mmap_mode='r')
            old_size = np.load(size_path, mmap_mode='r')
            old_N = len(old_parent)

            # 2. If the new N is larger, expand the arrays
            if self.N > old_N:
                # print(f"[*] Expanding arrays from {old_N} to {self.N}...")
                
                # Allocate new arrays
                new_parent = np.arange(self.N, dtype=np.int32)
                new_size = np.ones(self.N, dtype=np.int32)

                # Copy old data into the first portion
                new_parent[:old_N] = old_parent
                new_size[:old_N] = old_size

                # Overwrite the files on disk
                np.save(self.parent_path, new_parent)
                np.save(self.size_path, new_size)

            self.parent = np.load(self.parent_path, mmap_mode='r+')
            self.size = np.load(self.size_path, mmap_mode='r+')

            
        # 3. Scenario B: Array files don't exist OR are empty (0 bytes) -> Initialize
        else:
            np.save(self.parent_path, np.arange(self.N, dtype=np.int32))
            np.save(self.size_path, np.ones(self.N, dtype=np.int32))
            
            self.parent = np.load(self.parent_path, mmap_mode='r+')
            self.size = np.load(self.size_path, mmap_mode='r+')

        

    def get_parent_array(self) -> np.ndarray:
        return self.parent
    
    def get_size_array(self) -> np.ndarray:
        return self.size
    
    def get_N(self) -> int:
        return self.N

    def flush(self):
        """Forces any pending memory-mapped changes to sync with the disk."""
        if isinstance(self.parent, np.memmap):
            self.parent.flush()
        if isinstance(self.size, np.memmap):
            self.size.flush()

    def process_edge_list(self, edges: np.ndarray):
        """
        Ingests edges. Updates happen directly on the disk-backed memmap arrays.
        """
        if len(edges) == 0:
            return
            
        for u, v in edges:
            self._union(int(u), int(v))

        self.flush()

    def find(self, i: int) -> int:
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
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            return False

        if self.size[root_u] < self.size[root_v]:
            root_u, root_v = root_v, root_u

        self.parent[root_v] = root_u
        self.size[root_u] += self.size[root_v]
        return True