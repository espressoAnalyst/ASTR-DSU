import csv
import time


from src.dsu.string_dsu import StringDSU
from src.memory_analysis.ram_usage import get_ram_usage_mb  

def run_string_bucket(file_path):

    dsu = StringDSU()
    
    start_ram = get_ram_usage_mb()
    start_time = time.perf_counter()

    with open(file_path, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            u = row["u"]
            v = row["v"]

            dsu.union(u, v)
    end_time = time.perf_counter()
    end_ram = get_ram_usage_mb()

    execution_time = end_time - start_time

    ram_used = end_ram - start_ram

    components = dsu.get_components()

    print("\n===== PERFORMANCE =====\n")

    print(
        f"Execution Time: {execution_time:.6f} sec"
    )

    print(
        f"RAM Used: {ram_used:.4f} MB"
    )

    print("\n===== COMPONENTS =====\n")

    for root, nodes in components.items():
        print(root, "->", nodes)

    return components
