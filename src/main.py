import time
import os

from src.graph.graph_loader import load_edges
from src.dsu.dsu_basic import DSU

from src.memory_analysis.ram_usage import get_ram_usage_mb
from src.logging_system.logger import setup_logger
from src.logging_system.performance_monitor import save_performance_stats


def main(file_path):

    logger = setup_logger()

    logger.info("===== ASTR EXECUTION STARTED =====")

    start_time = time.time()
    start_ram = get_ram_usage_mb()

    logger.info(f"Loading dataset: {file_path}")

    edges = load_edges(file_path)

    logger.info(f"Total edges loaded: {len(edges)}")

    # -------------------------
    # DSU PROCESSING
    # -------------------------
    dsu = DSU()

    for u, v in edges:
        dsu.make_set(u)
        dsu.make_set(v)
        dsu.union(u, v)

    components = dsu.get_components()

    # -------------------------
    # METRICS CALCULATION
    # -------------------------
    end_time = time.time()
    end_ram = get_ram_usage_mb()

    execution_time = round(end_time - start_time, 4)
    ram_used = round(end_ram - start_ram, 4)

    total_edges = len(edges)

    throughput = (
        round(total_edges / execution_time, 2)
        if execution_time > 0 else 0
    )

    dataset_name = os.path.basename(file_path)

    # -------------------------
    # LOGGING
    # -------------------------
    logger.info(f"Execution Time: {execution_time} sec")
    logger.info(f"RAM Used: {ram_used} MB")
    logger.info(f"Connected Components: {len(components)}")
    logger.info(f"Throughput: {throughput} edges/sec")

    print("\n===== CONNECTED COMPONENTS =====\n")

    for root, nodes in components.items():
        print(f"{root} -> {nodes}")

    # -------------------------
    # BENCHMARK RECORD
    # -------------------------
    performance_data = {
        "algorithm": "basic",
        "dataset": dataset_name,
        "execution_time_sec": execution_time,
        "ram_used_mb": ram_used,
        "total_components": len(components),
        "total_edges": total_edges,
        "throughput": throughput
    }

    save_performance_stats(performance_data)

    logger.info("Performance stats saved")
    logger.info("===== ASTR EXECUTION FINISHED =====")


# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":

    main("data/dummy/small_graph.csv")