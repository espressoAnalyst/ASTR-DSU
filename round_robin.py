import os
import pickle
import numpy as np

def assign_centroids(centroids: np.ndarray, cmap: dict) -> None:
 
    # Create the output directory if it doesn't exist
    output_dir = "centroids"
    os.makedirs(output_dir, exist_ok=True)

    num_centroids = len(centroids)
    if num_centroids == 0:
        return

    # Extract cluster IDs (the keys of the cluster map)
    cluster_ids = list(cmap.keys())

    # Distribute cluster IDs via round-robin and save to individual pkl files
    for i, centroid_name in enumerate(centroids):
        # Python slicing with step size handles the round-robin
        assigned_cluster_id_keys = cluster_ids[i::num_centroids]

        assigned_members = []
        for key in assigned_cluster_id_keys:
           assigned_members.append(cmap[key])

        # File named after the centroid itself
        file_path = os.path.join(output_dir, f"centroid_{i}.bin")

        # Save ONLY the list of cluster IDs
        with open(file_path, "wb") as f:
            f.write(assigned_members) # to be checked
