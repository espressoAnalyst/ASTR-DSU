from typing import Generator, Tuple

from typing import Generator, Tuple

def stream_edges_from_disk(file_path: str) -> Generator[Tuple[str, str], None, None]:
    """
    Actually reads the massive dataset from the physical file on your disk,
    yielding one pair at a time to prevent RAM overload.
    """
    with open(file_path, 'r') as file:
        for line in file:
            # Skip empty lines just in case
            if not line.strip():
                continue
                
            # Split the CSV row into node1 and node2
            node1, node2 = line.strip().split(',')
            yield node1, node2