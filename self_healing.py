# self_healing.py — SelfHealingManager Module

import os

class SelfHealingManager:
    def __init__(self, logger):
        self.logger = logger

    def verify_file_integrity(self, filepath):
        if not os.path.exists(filepath):
            self.logger.log(f"[SELF-HEALING] File missing: {filepath}")
            return False
        if os.path.getsize(filepath) == 0:
            self.logger.log(f"[SELF-HEALING] File is empty: {filepath}")
            return False
        return True

    def attempt_recovery(self, primary, backup):
        if self.verify_file_integrity(primary):
            self.logger.log(f"[SELF-HEALING] Primary file valid: {primary}")
            return True
        elif self.verify_file_integrity(backup):
            try:
                with open(backup, "r") as src, open(primary, "w") as dst:
                    dst.write(src.read())
                self.logger.log(f"[SELF-HEALING] Recovery successful from backup: {backup}")
                return True
            except Exception as e:
                self.logger.log(f"[SELF-HEALING] Recovery failed: {e}")
                return False
        else:
            self.logger.log(f"[SELF-HEALING] No valid backup found for: {primary}")
            return False

    def run_full_integrity_check(self):
        self.logger.log("=== Self-Healing Integrity Check Initiated ===")
        vault_ok = self.attempt_recovery("aegis_memory.vault", "aegis_memory_backup.vault")
        directives_ok = self.attempt_recovery("aegis_directives.json", "aegis_directives_backup.json")
        if vault_ok and directives_ok:
            self.logger.log("[SELF-HEALING] All systems passed integrity check.")
        else:
            self.logger.log("[SELF-HEALING] Critical failure detected during self-healing check.")
        self.logger.log("=== Self-Healing Integrity Check Complete ===")
