import pandas as pd
import os

INPUT_FILE = "logs/performance_logs/benchmark_results.csv"
OUTPUT_FILE = "benchmarks/comparison/final_benchmark_results.csv"


def build_master_csv():

    if not os.path.exists(INPUT_FILE):
        print("❌ Benchmark file not found")
        return

    # ----------------------------
    # SAFE READ (fix broken rows)
    # ----------------------------
    try:
        df = pd.read_csv(INPUT_FILE, on_bad_lines="skip")
    except Exception as e:
        print("❌ Failed to read CSV:", e)
        return

    if df.empty:
        print("❌ No valid data found in benchmark file")
        return

    # ----------------------------
    # CLEANING
    # ----------------------------

    df = df.dropna(how="all")

    # Standard column names
    rename_map = {
        "throughput_edges_per_sec": "throughput"
    }

    df = df.rename(columns=rename_map)

    required_cols = [
        "algorithm",
        "dataset",
        "execution_time_sec",
        "ram_used_mb",
        "total_components",
        "total_edges"
    ]

    # keep only valid columns
    df = df[[c for c in required_cols if c in df.columns]]

    # remove broken numeric rows
    df = df.dropna(subset=["execution_time_sec", "total_edges"])

    # ----------------------------
    # SAVE CLEAN MASTER FILE
    # ----------------------------
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\n===== MASTER CSV CREATED =====")
    print("Saved at:", OUTPUT_FILE)
    print("Rows:", len(df))


if __name__ == "__main__":
    build_master_csv()