# logger.py — AegisLogger Module

import os
from datetime import datetime

class AegisLogger:
    def __init__(self, logfile="boot_log.txt"):
        self.logfile = logfile
        if not os.path.exists(self.logfile):
            with open(self.logfile, "w") as f:
                f.write("=== Aegis Prime Log ===\n")

    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {msg}"
        print(line)
        with open(self.logfile, "a") as f:
            f.write(line + "\n")
