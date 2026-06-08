import csv


def generate_edge_chunks(file_path, chunk_size=5):

    chunk = []

    with open(file_path, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            u = int(row["u"])
            v = int(row["v"])

            chunk.append((u, v))

            if len(chunk) >= chunk_size:

                yield chunk

                chunk = []

        if chunk:
            yield chunk