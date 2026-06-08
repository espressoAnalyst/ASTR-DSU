'''
import csv


def stream_edges(file_path):

    with open(file_path, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            u = int(row["u"])
            v = int(row["v"])

            yield u, v 
            '''
import csv


def stream_edges(file_path):

    with open(file_path, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            u = int(row["u"])
            v = int(row["v"])

            yield u, v


def get_max_node_id(file_path):

    max_node = 0

    for u, v in stream_edges(file_path):

        max_node = max(max_node, u, v)

    return max_node