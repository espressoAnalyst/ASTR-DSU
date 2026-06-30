from src.graph.edge_list_builder import EdgeListBuilder


def main():

    builder = EdgeListBuilder(
        bucket_folder="data/buckets",
        dtype="uint32",
        remove_duplicates=False
    )

    edge_list, metadata = builder.build()

    print("\nEdge List")
    print(edge_list)

    print("\nMetadata")
    for key, value in metadata.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()