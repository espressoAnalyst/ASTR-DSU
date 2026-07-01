import os

import numpy as np
from module_2 import GlobalArrayDSU
#from placeholder import N

N = 1000000  # Placeholder for the actual value of N
#edge list function to be modified when module_1 is complete
def get_edge_list(filepath: str) -> np.ndarray:
    """Fetches edges generated from Module 1."""
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        return np.load(filepath)
    
    

def main():
    # 1. Define Paths
    #N_PATH = "data/global_N.npy"
    PARENT_PATH = "data/global_parent.npy"
    SIZE_PATH = "data/global_size.npy"
    EDGES_PATH = "data/batch_edges.npy"

    # 2. Fetch edge list (from module 1)
    edges = get_edge_list(EDGES_PATH)

    # 3. Instantiate DSU
    dsu = GlobalArrayDSU(
        N = N, 
        parent_path=PARENT_PATH, 
        size_path=SIZE_PATH
    )

    # 4. Process the batch (Updates happen directly to the files via memmap)
    dsu.process_edge_list(edges, 
                          parent_path=PARENT_PATH, 
                          size_path=SIZE_PATH)

    # 5. Sync memmap changes strictly to disk
    dsu.flush()

if __name__ == "__main__":
    main()