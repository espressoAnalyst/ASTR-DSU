import os
import numpy as np
from module_2 import GlobalArrayDSU
from module_1 import EdgeListBuilder
#from placeholder import N

N = 1000000  # Placeholder for the actual value of N

#edge list function to be modified when module_1 is complete
def get_edge_list(filepath: str) -> np.ndarray:
    """Fetches edges generated from Module 1."""
    try:
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return np.load(filepath)
    except Exception as e:
        print(f"Error loading edge list from {filepath}: {e}")
            

    
def main():
    # 1. Define Paths
    #N_PATH = "data/global_N.npy"
    PARENT_PATH = "data/global_parent.npy"
    SIZE_PATH = "data/global_size.npy"
    #importing the bucket folder path for the edge list builder from module 1
    BUCKET_FOLDER = "data/buckets"
    
    #EDGES_PATH = "data/batch_edges.npy"

    # 2. Fetch edge list (from module 1)
    builder = EdgeListBuilder(
        bucket_folder=BUCKET_FOLDER,
        dtype="uint32",
        remove_duplicates=False
    )

    edge_list, metadata = builder.build()

    print("\nEdge List")
    print(edge_list)

    print("\nMetadata")
    for key, value in metadata.items():
        print(f"{key}: {value}")
    #edges = get_edge_list(EDGES_PATH)

    #For now, we will use the edge_list generated from module 1 as the edges to process
    #module 1 will require some modifications to save the edge list to a file, which will be used here in the future
    
    edges = edge_list

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