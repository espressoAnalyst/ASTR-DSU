import pandas as pd
import os

INPUT_FILE = "benchmarks/comparison/final_benchmark_results.csv"
OUTPUT_FILE = "benchmarks/comparison/clean_benchmark_results.csv"


def clean():

    if not os.path.exists(INPUT_FILE):
        print("❌ Benchmark file not found:", INPUT_FILE)
        return

    df = pd.read_csv(INPUT_FILE)

    # Remove invalid rows
    df = df[df["execution_time_sec"] > 0]
    df = df[df["total_edges"] > 0]

    # Normalize dataset names
    df["dataset"] = df["dataset"].replace({
        "small_graph.csv": "small",
        "medium_graph.csv": "medium",
        "large_graph.csv": "large"
    })

    # Remove duplicates
    df = df.drop_duplicates()

    required_cols = [
        "algorithm",
        "dataset",
        "execution_time_sec",
        "ram_used_mb",
        "total_components",
        "total_edges",
        "throughput_edges_per_sec"
    ]

    df = df[[c for c in required_cols if c in df.columns]]

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("\n===== CLEAN BENCHMARK CREATED =====")
    print("Saved at:", OUTPUT_FILE)
    print("Rows:", len(df))


if __name__ == "__main__":
    clean()