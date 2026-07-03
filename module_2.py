import os
import numpy as np
import psutil
import time

class ResourceTracker:
    """
    A context manager to track execution time and System RAM usage.
    """
    def __init__(self, operation_name: str, logger_func):
        self.operation_name = operation_name
        self.logger_func = logger_func
        self.process = psutil.Process(os.getpid())

    def __enter__(self):
        self.start_time = time.perf_counter()
        # Measure RSS (Resident Set Size) in MB
        self.start_ram = self.process.memory_info().rss / (1024 * 1024)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.perf_counter()
        end_ram = self.process.memory_info().rss / (1024 * 1024)

        elapsed_time = end_time - self.start_time
        ram_diff = end_ram - self.start_ram

        self.logger_func(
            f"{self.operation_name} -> Time: {elapsed_time:.4f}s | "
            f"RAM Change: {ram_diff:+.2f} MB | Total RAM: {end_ram:.2f} MB"
        )

class GlobalArrayDSU:
    def __init__(self, N: int, parent_path: str, size_path: str):
        """
        Initializes the DSU by memory-mapping arrays directly from disk.
        Safely handles pre-created 0-byte (empty) array files.
        """
        self.N = N
        self.parent_path = parent_path
        self.size_path = size_path


        with ResourceTracker("Init standard arrays", self.logger):
            self.parent = np.arange(self.N, dtype=np.int32)
            self.size = np.ones(self.N, dtype=np.int32)

        # Helper to check if array files exist AND have actual data in it
        def is_valid_file(filepath):
            return os.path.exists(filepath) and os.path.getsize(filepath) > 0

        
        if is_valid_file(parent_path) and is_valid_file(size_path):
            # 1. Load the old arrays in read-only mode to check their size
            old_parent = np.load(parent_path, mmap_mode='r')
            old_size = np.load(size_path, mmap_mode='r')
            old_N = len(old_parent)

            # 2. If the new N is larger, expand the arrays
            if self.N > old_N:

                # Copy old data into the first portion
                with ResourceTracker(f"Expand arrays ({old_N} to {self.N})", self.logger):
                    self.parent[:old_N] = old_parent
                    self.size[:old_N] = old_size

        
        # Overwrite the files on disk if paths exist
        if os.path.exists(self.parent_path):
            np.save(self.parent_path, self.parent)
        if os.path.exists(self.size_path):
            np.save(self.size_path, self.size)

    def logger(self, message: str):
        """Simple logger for debugging."""
        print(f"[GlobalArrayDSU] {message}")

    def get_parent_array(self) -> np.ndarray:
        return self.parent
    
    def get_size_array(self) -> np.ndarray:
        return self.size
    
    def get_N(self) -> int:
        return self.N
    
    def dump(self, parent_path: str, size_path: str):
        """Dumps the current state of the DSU to disk."""
        
        with ResourceTracker("Dump: Path Compression", self.logger):
            for i in range(self.N):
                if self.parent[i] != i:
                    self.find(i)  # Path compression    

        np.save(parent_path, self.parent)
        np.save(size_path, self.size)


    def process_edge_list(self, edges: np.ndarray):
        """
        Ingests edges. Updates happen directly on the disk-backed memmap arrays.
        """
        if len(edges) == 0:
            return
        
        with ResourceTracker(f"Process {len(edges)} edges", self.logger):    
            for u, v in edges:
                self._union(int(u), int(v))


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