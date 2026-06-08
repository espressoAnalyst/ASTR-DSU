import os
from datetime import datetime

from src.main import main as run_basic
from src.distributed.sequential_execution import run_optimized_sequential
from src.distributed.distributed_execution import run_distributed_sequential
from src.distributed.multiprocessing_execution import run_parallel_dsu


DATASETS = {
    "small": "data/dummy/small_graph.csv",
    "medium": "data/dummy/medium_graph.csv",
    "large": "data/dummy/large_graph.csv",
}


# --------------------------
# LOG FILE SETUP
# --------------------------
os.makedirs("logs/benchmark_runs", exist_ok=True)
log_file = "logs/benchmark_runs/run_log.txt"


def log(message):
    print(message)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def run_all():

    start_time = datetime.now()

    log("\n===== ASTR BENCHMARK STARTED =====")
    log(f"Start Time: {start_time}\n")

    for dataset_name, path in DATASETS.items():

        log(f"\n========== DATASET: {dataset_name.upper()} ==========\n")

        log("Running BASIC DSU...")
        run_basic(path)

        log("Running OPTIMIZED SEQUENTIAL DSU...")
        run_optimized_sequential(path)

        log("Running DISTRIBUTED SEQUENTIAL DSU...")
        run_distributed_sequential(path)

        log("Running PARALLEL DSU...")
        run_parallel_dsu(path)

    end_time = datetime.now()

    log("\n===== ALL 12 EXPERIMENTS COMPLETED =====")
    log(f"End Time: {end_time}")
    log(f"Total Duration: {end_time - start_time}\n")


if __name__ == "__main__":
    run_all()