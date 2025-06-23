import os
import psutil
import socket
import hashlib
import time
import threading

class MultiVectorSentinel:
    def __init__(self, logger):
        self.logger = logger
        self.monitored_files = {}  # {path: sha256_hash}
        self.active_monitoring = False

    # ===================== FILE SYSTEM MONITORING =====================

    def register_file_for_monitoring(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            self.monitored_files[file_path] = file_hash
            self.logger.log(f"File registered for monitoring: {file_path}")
        else:
            self.logger.log(f"File not found for monitoring: {file_path}")

    def scan_file_integrity(self):
        for file_path, original_hash in self.monitored_files.items():
            if not os.path.isfile(file_path):
                self.logger.log(f"Monitored file missing: {file_path}")
                continue
            with open(file_path, 'rb') as f:
                new_hash = hashlib.sha256(f.read()).hexdigest()
            if new_hash != original_hash:
                self.logger.log(f"FILE INTEGRITY VIOLATION detected: {file_path}")

    # ===================== PROCESS MONITORING =====================

    def scan_running_processes(self):
        suspicious = []
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                proc_info = proc.info
                if not proc_info['exe']:
                    continue
                if not os.path.exists(proc_info['exe']):
                    suspicious.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if suspicious:
            for proc in suspicious:
                self.logger.log(f"Suspicious process detected: {proc}")
        else:
            self.logger.log("No suspicious processes detected.")

    # ===================== NETWORK MONITORING =====================

    def scan_network_ports(self):
        connections = psutil.net_connections()
        for conn in connections:
            if conn.status == 'ESTABLISHED':
                try:
                    laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
                    raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "NONE"
                    self.logger.log(f"Active connection: {laddr} -> {raddr}")
                except Exception:
                    continue

    # ===================== CONTINUOUS SENTINEL =====================

    def start_continuous_monitoring(self, interval_seconds=30):
        if self.active_monitoring:
            self.logger.log("Multi-Vector Sentinel already active.")
            return

        self.logger.log("Starting continuous multi-vector monitoring...")
        self.active_monitoring = True
        threading.Thread(target=self._sentinel_loop, args=(interval_seconds,), daemon=True).start()

    def _sentinel_loop(self, interval_seconds):
        while self.active_monitoring:
            self.logger.log("Multi-Vector Sentinel Sweep Running...")
            self.scan_file_integrity()
            self.scan_running_processes()
            self.scan_network_ports()
            time.sleep(interval_seconds)

    def stop_monitoring(self):
        self.active_monitoring = False
        self.logger.log("Multi-Vector Sentinel Monitoring Stopped.")
