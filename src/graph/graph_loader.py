import csv


def load_edges(file_path):
    edges = []

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            u = int(row["u"])
            v = int(row["v"])

            edges.append((u, v))

    return edges