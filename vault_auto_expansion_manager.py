import os
import shutil
import time
import threading

class VaultAutoExpansionManager:
    def __init__(self, logger, vault_manager, check_interval_seconds=300, threshold_percent=80):
        self.logger = logger
        self.vault_manager = vault_manager
        self.check_interval = check_interval_seconds
        self.threshold_percent = threshold_percent
        self.running = False

    def start_monitoring(self):
        self.running = True
        thread = threading.Thread(target=self._monitor_loop, daemon=True)
        thread.start()
        self.logger.log("Vault Auto Expansion Monitoring started.")

    def stop_monitoring(self):
        self.running = False
        self.logger.log("Vault Auto Expansion Monitoring stopped.")

    def _monitor_loop(self):
        while self.running:
            try:
                self._check_and_expand_if_needed()
            except Exception as e:
                self.logger.log(f"Vault Auto Expansion error: {str(e)}")
            time.sleep(self.check_interval)

    def _check_and_expand_if_needed(self):
        vault_path = self.vault_manager.get_vault_path()
        total, used, free = shutil.disk_usage(vault_path)
        used_percent = (used / total) * 100

        self.logger.log(f"Vault Storage Usage: {used_percent:.2f}% used.")

        if used_percent >= self.threshold_percent:
            self.logger.log("Vault nearing capacity. Initiating expansion protocol.")
            self._expand_vault(vault_path)

    def _expand_vault(self, vault_path):
        # Placeholder for actual expansion logic.
        # In real deployment, this might link additional storage, cloud resources or external drives.

        expansion_path = os.path.join(vault_path, "expansion_segment")
        if not os.path.exists(expansion_path):
            os.makedirs(expansion_path)
            self.logger.log(f"Vault Expansion: Created additional expansion segment at {expansion_path}")
        else:
            self.logger.log(f"Vault Expansion: Expansion segment already exists at {expansion_path}")
