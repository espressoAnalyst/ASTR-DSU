import time
import os

from src.graph.graph_partition import generate_edge_chunks
from src.graph.graph_utils import get_max_node_id

from src.dsu.dsu_optimized import OptimizedDSU

from src.memory_analysis.ram_usage import get_ram_usage_mb
from src.logging_system.logger import setup_logger
from src.logging_system.performance_monitor import save_performance_stats


def run_distributed_sequential(file_path):

    logger = setup_logger()

    logger.info("===== DISTRIBUTED SEQUENTIAL EXECUTION STARTED =====")

    start_time = time.time()
    start_ram = get_ram_usage_mb()

    # -------------------------
    # GRAPH PREPROCESSING
    # -------------------------
    max_nodes = get_max_node_id(file_path) + 1

    logger.info(f"Detected Max Node ID: {max_nodes - 1}")

    global_dsu = OptimizedDSU(max_nodes=max_nodes)

    chunk_size = 5

    total_edges = 0
    total_chunks = 0

    # -------------------------
    # CHUNK PROCESSING
    # -------------------------
    for chunk in generate_edge_chunks(file_path, chunk_size):

        logger.info(f"Processing chunk {total_chunks + 1}")

        for u, v in chunk:
            global_dsu.union(u, v)
            total_edges += 1

        total_chunks += 1

    components = global_dsu.get_components()

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
        round(total_edges / execution_time, 2)
        if execution_time > 0 else 0
    )

    dataset = "small"   # standardized for benchmarking

    # -------------------------
    # LOGGING
    # -------------------------
    logger.info(f"Execution Time: {execution_time} sec")
    logger.info(f"RAM Used: {ram_used} MB")
    logger.info(f"Edges Processed: {total_edges}")
    logger.info(f"Chunks Processed: {total_chunks}")
    logger.info(f"Throughput: {throughput} edges/sec")

    print("\n===== DISTRIBUTED SEQUENTIAL COMPONENTS =====\n")

    for root, nodes in filtered_components.items():
        print(f"{root} -> {nodes}")

    # -------------------------
    # BENCHMARK RECORD
    # -------------------------
    performance_data = {
        "algorithm": "distributed_sequential",
        "dataset": dataset,
        "execution_time_sec": execution_time,
        "ram_used_mb": ram_used,
        "total_components": len(filtered_components),
        "total_edges": total_edges,
        "throughput": throughput,
        "chunks_processed": total_chunks
    }

    save_performance_stats(performance_data)

    logger.info("===== DISTRIBUTED SEQUENTIAL EXECUTION FINISHED =====")


if __name__ == "__main__":

    run_distributed_sequential("data/dummy/small_graph.csv")