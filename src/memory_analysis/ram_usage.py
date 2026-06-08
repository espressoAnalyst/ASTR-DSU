import os
import psutil


def get_ram_usage_mb():

    process = psutil.Process(os.getpid())

    memory_bytes = process.memory_info().rss

    memory_mb = memory_bytes / (1024 * 1024)

    return round(memory_mb, 4)