import psutil
import time
import os

class ResourceTracker:
    """
    A context manager to track execution time and System RAM usage.
    """
    def __init__(self, operation_name: str, logger_func):
        self.operation_name = operation_name
        self.logger_func = logger_func
        self.process = psutil.Process(os.getpid())

    def __enter__(self):
        self.start_time = time.perf_counter()
        # Measure RSS (Resident Set Size) in MB
        self.start_ram = self.process.memory_info().rss / (1024 * 1024)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.perf_counter()
        end_ram = self.process.memory_info().rss / (1024 * 1024)

        elapsed_time = end_time - self.start_time
        ram_diff = end_ram - self.start_ram

        # Calculate percentage change based on the starting RAM of this block
        if self.start_ram > 0:
            ram_percent_change = (ram_diff / self.start_ram) * 100
        else:
            ram_percent_change = 0.0

        if exc_type is not None:
            self.logger_func(f"⚠️ {self.operation_name} FAILED due to: {exc_type.__name__}")

        self.logger_func(
            f"{self.operation_name} -> Time: {elapsed_time:.4f}s | "
            f"RAM Change: {ram_percent_change:+.2f}% | Process RAM: {end_ram:.2f} MB"
        )