import numpy as np

edges = np.fromfile(
    "data/buckets/bucket_001.bin",
    dtype=np.uint32
)

edges = edges.reshape(-1, 2)

print(edges)