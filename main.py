from src.graph.edge_list_builder import EdgeListBuilder
import numpy as np


def main():

    builder = EdgeListBuilder(
        bucket_folder="data/buckets",
        output_folder="data/generated",
        output_name="combined_edge_list",
        dtype=np.uint64
    )

    edge_list, metadata = builder.build()

    print("\nCombined Edge List")
    print(edge_list)

    print("\nMetadata")
    for key, value in metadata.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()