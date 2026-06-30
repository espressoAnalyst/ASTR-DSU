import os
import numpy as np

# ------------------------------------

OUTPUT_FOLDER = "data/buckets"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ------------------------------------
# Bucket 1
# ------------------------------------

bucket1 = np.array(
    [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5]
    ],
    dtype=np.uint32
)

# ------------------------------------
# Bucket 2
# ------------------------------------

bucket2 = np.array(
    [
        [6, 7],
        [7, 8],
        [8, 9]
    ],
    dtype=np.uint32
)

# ------------------------------------
# Bucket 3
# ------------------------------------

bucket3 = np.array(
    [
        [3, 6],
        [10, 11],
        [11, 12]
    ],
    dtype=np.uint32
)

# ------------------------------------
# Save Buckets
# ------------------------------------

bucket1.tofile(
    os.path.join(
        OUTPUT_FOLDER,
        "bucket_001.bin"
    )
)

bucket2.tofile(
    os.path.join(
        OUTPUT_FOLDER,
        "bucket_002.bin"
    )
)

bucket3.tofile(
    os.path.join(
        OUTPUT_FOLDER,
        "bucket_003.bin"
    )
)

print("Dummy binary buckets created successfully.")