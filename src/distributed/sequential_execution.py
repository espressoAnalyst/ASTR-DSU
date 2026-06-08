import time
import os

from src.dsu.dsu_optimized import OptimizedDSU
from src.graph.graph_utils import (
    stream_edges,
    get_max_node_id
)

from src.memory_analysis.ram_usage import get_ram_usage_mb
from src.logging_system.logger import setup_logger
from src.logging_system.performance_monitor import save_performance_stats


def run_optimized_sequential(file_path):

    logger = setup_logger()

    logger.info("===== OPTIMIZED SEQUENTIAL EXECUTION STARTED =====")

    start_time = time.time()
    start_ram = get_ram_usage_mb()

    # -------------------------
    # LOAD + PREPROCESS
    # -------------------------
    max_nodes = get_max_node_id(file_path) + 1

    logger.info(f"Detected Max Node ID: {max_nodes - 1}")

    dsu = OptimizedDSU(max_nodes=max_nodes)

    edge_count = 0

    # -------------------------
    # STREAM PROCESSING
    # -------------------------
    for u, v in stream_edges(file_path):
        dsu.union(u, v)
        edge_count += 1

    components = dsu.get_components()

    filtered_components = {
        root: nodes
        for root, nodes in components.items()
        if len(nodes) > 1
    }

    # -------------------------
    # METRICS
    # -------------------------
    end_time = time.time()
    end_ram = get_ram_usage_mb()

    execution_time = round(end_time - start_time, 4)
    ram_used = round(end_ram - start_ram, 4)

    throughput = (
        round(edge_count / execution_time, 2)
        if execution_time > 0 else 0
    )

    dataset = "small"   # IMPORTANT: standardized label (not filename)

    # -------------------------
    # LOGGING
    # -------------------------
    logger.info(f"Execution Time: {execution_time} sec")
    logger.info(f"RAM Used: {ram_used} MB")
    logger.info(f"Edges Processed: {edge_count}")
    logger.info(f"Components Found: {len(filtered_components)}")
    logger.info(f"Throughput: {throughput} edges/sec")

    print("\n===== OPTIMIZED COMPONENTS =====\n")

    for root, nodes in filtered_components.items():
        print(f"{root} -> {nodes}")

    # -------------------------
    # BENCHMARK RECORD
    # -------------------------
    performance_data = {
        "algorithm": "optimized_sequential",
        "dataset": dataset,
        "execution_time_sec": execution_time,
        "ram_used_mb": ram_used,
        "total_components": len(filtered_components),
        "total_edges": edge_count,
        "throughput": throughput
    }

    save_performance_stats(performance_data)

    logger.info("===== OPTIMIZED EXECUTION FINISHED =====")


if __name__ == "__main__":

    run_optimized_sequential("data/dummy/small_graph.csv")