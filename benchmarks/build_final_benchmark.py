import pandas as pd
import os

INPUT_FILE = "logs/performance_logs/sequential_stats.csv"
OUTPUT_FILE = "benchmarks/comparison/final_benchmark_results.csv"


def build_final_benchmark():

    if not os.path.exists(INPUT_FILE):
        print("❌ No logs found in performance_logs/")
        return

    df = pd.read_csv(INPUT_FILE)

    # ---------------- CLEANING ----------------
    df = df.dropna(how="all")

    # Fix column naming inconsistencies
    df = df.rename(columns={
        "throughput_edges_per_sec": "throughput"
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

    # Keep only valid columns
    df = df[[c for c in required_cols if c in df.columns]]

    df = df.dropna(subset=["execution_time_sec", "total_edges"])

    # Ensure numeric correctness
    for col in ["execution_time_sec", "ram_used_mb", "total_edges", "throughput"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()

    # ---------------- SAVE ----------------
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\n===== FINAL BENCHMARK FILE CREATED =====")
    print(f"Saved at: {OUTPUT_FILE}")
    print(f"Rows: {len(df)}")


if __name__ == "__main__":
    build_final_benchmark()