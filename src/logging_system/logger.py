import logging
import os


def setup_logger():

    os.makedirs("logs/execution_logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/execution_logs/run_001.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging