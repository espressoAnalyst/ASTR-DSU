import pandas as pd
import os

INPUT_FILE = "logs/performance_logs/sequential_stats.csv"
OUTPUT_FILE = "benchmarks/comparison/final_benchmark_results.csv"


def finalize():

    if not os.path.exists(INPUT_FILE):
        print("❌ No logs found")
        return

    df = pd.read_csv(INPUT_FILE)

    # Remove bad rows
    df = df.dropna(how="all")

    # Fix naming
    df = df.rename(columns={
        "throughput_edges_per_sec": "throughput"
    })

    # Keep only valid rows
    df = df[df["execution_time_sec"] > 0]
    df = df[df["total_edges"] > 0]

    # Normalize dataset names
    df["dataset"] = df["dataset"].replace({
        "small_graph.csv": "small",
        "medium_graph.csv": "medium",
        "large_graph.csv": "large"
    })

    required_cols = [
        "algorithm",
        "dataset",
        "execution_time_sec",
        "ram_used_mb",
        "total_components",
        "total_edges",
        "throughput"
    ]

    df = df[[c for c in required_cols if c in df.columns]]

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("\n===== FINAL BENCHMARK CREATED =====")
    print("Saved at:", OUTPUT_FILE)
    print("Rows:", len(df))


if __name__ == "__main__":
    finalize()