from pathlib import Path
import numpy as np


class EdgeListBuilder:

    def __init__(
        self,
        bucket_folder,
        dtype=np.uint32,
        remove_duplicates=False
    ):
        self.bucket_folder = Path(bucket_folder)
        self.dtype = np.dtype(dtype)
        self.remove_duplicates = remove_duplicates

        self.bucket_files = []
        self.total_edges = 0
        self.edge_array = None
        self.metadata = {}
        self.current_position = 0

    def _discover_buckets(self):
        self.bucket_files = sorted(self.bucket_folder.glob("*.bin"))

        if not self.bucket_files:
            raise FileNotFoundError(
                f"No binary bucket files found in {self.bucket_folder}"
            )

        print(f"Found {len(self.bucket_files)} bucket(s)")

    def _validate_bucket(self, bucket_path):
        if not bucket_path.exists():
            raise FileNotFoundError(
                f"{bucket_path.name} not found."
            )

        file_size = bucket_path.stat().st_size

        if file_size == 0:
            raise ValueError(
                f"{bucket_path.name} is empty."
            )

        bytes_per_edge = self.dtype.itemsize * 2

        if file_size % bytes_per_edge != 0:
            raise ValueError(
                f"{bucket_path.name} is corrupted."
            )

        return file_size

    def _count_total_edges(self):
        self.total_edges = 0

        bytes_per_edge = self.dtype.itemsize * 2

        for bucket in self.bucket_files:
            file_size = self._validate_bucket(bucket)
            num_edges = file_size // bytes_per_edge
            self.total_edges += num_edges

            print(
                f"{bucket.name} : {num_edges} edges"
            )

        print(f"Total Edges : {self.total_edges}")

    def _allocate_global_array(self):
        self.edge_array = np.empty(
            (self.total_edges, 2),
            dtype=self.dtype
        )

        print(
            f"Allocated {self.edge_array.nbytes/(1024**2):.4f} MB"
        )

    def _read_bucket(self, bucket_path):
        bucket_edges = np.fromfile(
            bucket_path,
            dtype=self.dtype
        )

        if bucket_edges.size % 2 != 0:
            raise ValueError(
                f"{bucket_path.name} contains incomplete edge."
            )

        bucket_edges = bucket_edges.reshape(-1, 2)

        return bucket_edges

    def _merge_bucket(self, bucket_edges):
        num_edges = len(bucket_edges)

        start = self.current_position
        end = start + num_edges

        if end > self.total_edges:
            raise RuntimeError(
                "Edge array overflow."
            )

        self.edge_array[start:end] = bucket_edges

        self.current_position = end

    def _remove_duplicate_edges(self):
        before = len(self.edge_array)

        self.edge_array = np.sort(
            self.edge_array,
            axis=1
        )

        self.edge_array = np.unique(
            self.edge_array,
            axis=0
        )

        self.total_edges = len(self.edge_array)

        after = len(self.edge_array)

        print(
            f"Duplicate Removal : {before-after} removed"
        )

    def _generate_metadata(self):
        self.metadata = {
            "num_buckets": len(self.bucket_files),
            "num_edges": self.total_edges,
            "array_shape": self.edge_array.shape,
            "dtype": str(self.edge_array.dtype),
            "memory_bytes": int(self.edge_array.nbytes),
            "memory_mb": round(
                self.edge_array.nbytes / (1024 ** 2),
                4
            ),
            "bucket_folder": str(self.bucket_folder),
            "duplicates_removed": self.remove_duplicates
        }

    def build(self):
        self.current_position = 0

        self._discover_buckets()

        self._count_total_edges()

        self._allocate_global_array()

        for bucket in self.bucket_files:
            edges = self._read_bucket(bucket)
            self._merge_bucket(edges)

        if self.remove_duplicates:
            self._remove_duplicate_edges()

        self._generate_metadata()

        return self.edge_array, self.metadata