import time
from multiprocessing import Pool, cpu_count

from src.graph.graph_partition import generate_edge_chunks
from src.graph.graph_utils import get_max_node_id
from src.dsu.dsu_optimized import OptimizedDSU

from src.memory_analysis.ram_usage import get_ram_usage_mb
from src.logging_system.logger import setup_logger
from src.logging_system.performance_monitor import save_performance_stats


# ---------------------------
# Worker function
# ---------------------------
def process_chunk(chunk):

    max_node = 0

    for u, v in chunk:
        max_node = max(max_node, u, v)

    local_dsu = OptimizedDSU(max_node + 1)

    for u, v in chunk:
        local_dsu.union(u, v)

    return chunk


# ---------------------------
# Main execution
# ---------------------------
def run_parallel_dsu(file_path):

    logger = setup_logger()

    logger.info("===== PARALLEL DSU STARTED =====")

    start_time = time.time()
    start_ram = get_ram_usage_mb()

    chunk_size = 5

    chunks = list(generate_edge_chunks(file_path, chunk_size))

    total_chunks = len(chunks)

    workers = min(cpu_count(), total_chunks)

    logger.info(f"Workers Used: {workers}")
    logger.info(f"Chunks Created: {total_chunks}")

    # Parallel processing
    with Pool(processes=workers) as pool:
        results = pool.map(process_chunk, chunks)

    # Global merge phase
    max_nodes = get_max_node_id(file_path) + 1

    logger.info(f"Detected Max Node ID: {max_nodes - 1}")

    global_dsu = OptimizedDSU(max_nodes)

    total_edges = 0

    for chunk_edges in results:
        for u, v in chunk_edges:
            global_dsu.union(u, v)
            total_edges += 1

    components = global_dsu.get_components()

    filtered_components = {
        root: nodes
        for root, nodes in components.items()
        if len(nodes) > 1
    }

    # ---------------------------
    # Metrics
    # ---------------------------
    end_time = time.time()
    end_ram = get_ram_usage_mb()

    execution_time = round(end_time - start_time, 4)
    ram_used = round(end_ram - start_ram, 4)

    throughput = (
        round(total_edges / execution_time, 2)
        if execution_time > 0 else 0
    )

    dataset = "small"

    # ---------------------------
    # Logging
    # ---------------------------
    logger.info(f"Execution Time: {execution_time} sec")
    logger.info(f"RAM Used: {ram_used} MB")
    logger.info(f"Edges Processed: {total_edges}")
    logger.info(f"Components Found: {len(filtered_components)}")
    logger.info(f"Throughput: {throughput}")

    # ---------------------------
    # Benchmark record (STANDARDIZED)
    # ---------------------------
    performance_data = {
        "algorithm": "parallel_dsu",
        "dataset": dataset,
        "execution_time_sec": execution_time,
        "ram_used_mb": ram_used,
        "total_components": len(filtered_components),
        "total_edges": total_edges,
        "chunks_processed": total_chunks,
        "workers_used": workers,
        "throughput": throughput
    }

    save_performance_stats(performance_data)

    # ---------------------------
    # Output
    # ---------------------------
    print("\n===== PARALLEL COMPONENTS =====\n")

    for root, nodes in filtered_components.items():
        print(f"{root} -> {nodes}")

    logger.info("===== PARALLEL DSU FINISHED =====")


# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    run_parallel_dsu("data/dummy/small_graph.csv")