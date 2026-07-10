from pathlib import Path
import numpy as np


class EdgeListBuilder:

    def __init__(
        self,
        bucket_folder,
        output_folder,
        output_name="combined_edge_list",
        dtype=np.uint64
    ):
        self.bucket_folder = Path(bucket_folder)
        self.output_folder = Path(output_folder)
        self.output_name = output_name
        self.dtype = np.dtype(dtype)

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.bucket_files = []
        self.edge_set = set()
        self.total_edges = 0
        self.edge_array = None
        self.metadata = {}

    def _discover_buckets(self):
        self.bucket_files = sorted(
            self.bucket_folder.glob("*.bin")
        )

        if not self.bucket_files:
            raise FileNotFoundError(
                f"No binary bucket files found in {self.bucket_folder}"
            )

        print(
            f"Found {len(self.bucket_files)} bucket(s)"
        )

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

    def _read_bucket(self, bucket_path):
        bucket_edges = np.fromfile(
            bucket_path,
            dtype=self.dtype
        )

        if bucket_edges.size % 2 != 0:
            raise ValueError(
                f"{bucket_path.name} contains incomplete edge."
            )

        return bucket_edges.reshape(-1, 2)

    def _read_and_deduplicate(self):
        self.edge_set.clear()

        for bucket in self.bucket_files:

            self._validate_bucket(bucket)

            bucket_edges = self._read_bucket(bucket)

            print(
                f"{bucket.name} : {len(bucket_edges)} edges"
            )

            for u, v in bucket_edges:

                edge = (
                    int(min(u, v)),
                    int(max(u, v))
                )

                self.edge_set.add(edge)

        self.total_edges = len(self.edge_set)

        print(
            f"Unique Edges : {self.total_edges}"
        )

    def _build_edge_array(self):
        self.edge_array = np.array(
            list(self.edge_set),
            dtype=self.dtype
        )

        print(
            f"Allocated {self.edge_array.nbytes/(1024**2):.4f} MB"
        )

    def _save_npy(self):
        npy_path = self.output_folder / f"{self.output_name}.npy"

        np.save(
            npy_path,
            self.edge_array
        )

        return npy_path

    def _save_bin(self):
        bin_path = self.output_folder / f"{self.output_name}.bin"

        self.edge_array.tofile(
            bin_path
        )

        return bin_path

    def _generate_metadata(
        self,
        npy_path,
        bin_path
    ):
        self.metadata = {
            "num_buckets": len(self.bucket_files),
            "unique_edges": self.total_edges,
            "array_shape": self.edge_array.shape,
            "dtype": str(self.edge_array.dtype),
            "memory_bytes": int(self.edge_array.nbytes),
            "memory_mb": round(
                self.edge_array.nbytes / (1024 ** 2),
                4
            ),
            "bucket_folder": str(self.bucket_folder),
            "output_folder": str(self.output_folder),
            "edge_list_npy_path": str(npy_path),
            "edge_list_bin_path": str(bin_path)
        }

    def build(self):

        self._discover_buckets()

        self._read_and_deduplicate()

        self._build_edge_array()

        npy_path = self._save_npy()

        bin_path = self._save_bin()

        self._generate_metadata(
            npy_path,
            bin_path
        )

        return self.edge_array, self.metadata