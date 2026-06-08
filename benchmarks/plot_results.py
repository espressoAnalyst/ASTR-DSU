import pandas as pd
import matplotlib.pyplot as plt
import os

INPUT_FILE = "benchmarks/comparison/final_benchmark_results.csv"


def load_data():
    if not os.path.exists(INPUT_FILE):
        print("❌ No benchmark file found")
        return None
    return pd.read_csv(INPUT_FILE)


def plot_execution_time(df):

    plt.figure()

    for algo in df["algorithm"].unique():
        subset = df[df["algorithm"] == algo]
        plt.plot(subset["dataset"], subset["execution_time_sec"], marker="o", label=algo)

    plt.title("Execution Time Comparison")
    plt.xlabel("Dataset")
    plt.ylabel("Time (sec)")
    plt.legend()
    plt.grid()
    plt.show()


def plot_memory(df):

    plt.figure()

    for algo in df["algorithm"].unique():
        subset = df[df["algorithm"] == algo]
        plt.plot(subset["dataset"], subset["ram_used_mb"], marker="o", label=algo)

    plt.title("RAM Usage Comparison")
    plt.xlabel("Dataset")
    plt.ylabel("Memory (MB)")
    plt.legend()
    plt.grid()
    plt.show()


def plot_throughput(df):

    if "throughput_edges_per_sec" not in df.columns:
        print("⚠️ Throughput column missing — skipping throughput plot")
        return

    plt.figure()

    for algo in df["algorithm"].unique():
        subset = df[df["algorithm"] == algo]
        plt.plot(subset["dataset"], subset["throughput_edges_per_sec"], marker="o", label=algo)

    plt.title("Throughput Comparison")
    plt.xlabel("Dataset")
    plt.ylabel("Edges/sec")
    plt.legend()
    plt.grid()
    plt.show()


def main():

    df = load_data()
    if df is None:
        return

    print("📊 Generating Benchmark Graphs...")

    plot_execution_time(df)
    plot_memory(df)
    plot_throughput(df)


if __name__ == "__main__":
    main()