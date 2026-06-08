import pandas as pd
import os

LOG_FILE = "logs/performance_logs/benchmark_results.csv"


def save_performance_stats(data):

    os.makedirs("logs/performance_logs", exist_ok=True)

    df = pd.DataFrame([data])

    # Ensure consistent column order (VERY IMPORTANT for clean CSV)
    preferred_order = [
        "algorithm",
        "dataset",
        "execution_time_sec",
        "ram_used_mb",
        "total_components",
        "total_edges",
        "chunks_processed",
        "workers_used",
        "throughput_edges_per_sec"
    ]

    # Reorder safely
    df = df[[col for col in preferred_order if col in df.columns]]

    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_FILE, index=False)