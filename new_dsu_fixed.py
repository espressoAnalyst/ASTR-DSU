# import os
# import numpy as np

# class GlobalArrayDSU:
#     def __init__(self, N: int = None, parent: np.ndarray = None, size: np.ndarray = None, 
#                  n_path: str = None, parent_path: str = None, size_path: str = None):
#         """
#         Initializes the DSU. Supports direct array injection OR internal disk-backed memmap loading.
#         """
#         self.n_path = n_path
#         self.parent_path = parent_path
#         self.size_path = size_path

#         # Scenario A: Load directly from disk if paths are provided and files exist
#         if (n_path and os.path.exists(n_path) and 
#             parent_path and os.path.exists(parent_path) and 
#             size_path and os.path.exists(size_path)):
            
#             self.N = int(np.load(n_path))
#             self.parent = np.load(parent_path, mmap_mode='r+')
#             self.size = np.load(size_path, mmap_mode='r+')

#         # Scenario B: Arrays passed directly (RAM or externally loaded)
#         elif parent is not None and size is not None:
#             self.parent = parent
#             self.size = size
#             self.N = N if N is not None else len(parent)

#         # Scenario C: Initialize fresh arrays (and optionally save all to disk immediately)
#         elif N is not None:
#             self.N = N
#             self.parent = np.arange(self.N, dtype=np.int32)
#             self.size = np.ones(self.N, dtype=np.int32)
            
#             # If paths were provided, write to disk and switch arrays to memmap mode
#             if n_path and parent_path and size_path:
#                 np.save(self.n_path, np.array(self.N))
#                 np.save(self.parent_path, self.parent)
#                 np.save(self.size_path, self.size)
                
#                 self.parent = np.load(self.parent_path, mmap_mode='r+')
#                 self.size = np.load(self.size_path, mmap_mode='r+')
#         else:
#             raise ValueError("Must provide either existing file paths, existing arrays, or an N value.")

#         self.embedding_hashmap = {}

#     def flush_to_disk(self):
#         """
#         Syncs memmap changes back to disk. 
#         Safely does nothing if the arrays are strictly in standard RAM.
#         """
#         if isinstance(self.parent, np.memmap):
#             self.parent.flush()
#         if isinstance(self.size, np.memmap):
#             self.size.flush()

#     def process_edge_list(self, edges: np.ndarray):
#         if len(edges) == 0:
#             return
#         for u, v in edges:
#             self._union(int(u), int(v))

#     def find(self, i: int) -> int:
#         if i >= self.N:
#             return -1 
            
#         root = i
#         while root != self.parent[root]:
#             root = self.parent[root]
            
#         curr = i
#         while curr != root:
#             curr, self.parent[curr] = self.parent[curr], root
            
#         return root

#     def _union(self, u: int, v: int) -> bool:
#         root_u = self.find(u)
#         root_v = self.find(v)

#         if root_u == root_v:
#             return False

#         if self.size[root_u] < self.size[root_v]:
#             root_u, root_v = root_v, root_u

#         self.parent[root_v] = root_u
#         self.size[root_u] += self.size[root_v]
#         return True