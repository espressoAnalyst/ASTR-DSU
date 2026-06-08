import csv
import random
import os


def generate_graph(file_path, nodes, edges):

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    seen = set()

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["u", "v"])

        while len(seen) < edges:

            u = random.randint(0, nodes - 1)
            v = random.randint(0, nodes - 1)

            if u == v:
                continue

            edge = (min(u, v), max(u, v))

            if edge not in seen:
                seen.add(edge)
                writer.writerow([u, v])


if __name__ == "__main__":

    print("Generating MEDIUM dataset...")
    generate_graph(
        "data/dummy/medium_graph.csv",
        nodes=5000,
        edges=25000
    )

    print("Generating LARGE dataset...")
    generate_graph(
        "data/dummy/large_graph.csv",
        nodes=50000,
        edges=250000
    )

    print("DONE: All datasets generated")