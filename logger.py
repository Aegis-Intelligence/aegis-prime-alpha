# logger.py — Aegis Prime Unified Logging Module

import datetime
import os

class Logger:
    def __init__(self, log_file="aegis_system_log.txt"):
        self.log_file = log_file

        # Create initial session header if new log
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("=== Aegis Prime Sovereign System Log ===\n")
        else:
            with open(self.log_file, "a") as f:
                f.write("\n=== New Sovereign Session Started: "
                        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        print(entry)
        with open(self.log_file, "a") as f:
            f.write(entry + "\n")
