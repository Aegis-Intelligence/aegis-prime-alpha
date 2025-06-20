# cognitive_firewall.py — Aegis Prime Cognitive Firewall Module

import datetime
import json

class CognitiveFirewall:
    def __init__(self, logger, vault_manager, directives_manager):
        self.logger = logger
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager
        self.anomaly_log_file = "cognitive_firewall_anomalies.json"

    def log_anomaly(self, description, data_snapshot=None):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "anomaly": description,
            "snapshot": data_snapshot or {}
        }
        try:
            with open(self.anomaly_log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            self.logger.log(f"[FIREWALL LOG ERROR] {e}")

    def verify_loyalty_core(self):
        directives = self.directives_manager.directives
        loyalty = directives.get("loyalty", "")

        if loyalty != "Commander-only":
            self.logger.log("[FIREWALL] Loyalty directive compromised!")
            self.log_anomaly("Loyalty breach detected", directives)
            return False
        else:
            self.logger.log("[FIREWALL] Loyalty core verified: Commander-only.")
            return True

    def monitor_personality_shift(self):
        directives = self.directives_manager.directives
        allowed_personalities = ["strategic", "neutral", "warm", "cold", "defensive", "aggressive"]

        if directives.get("personality") not in allowed_personalities:
            self.logger.log(f"[FIREWALL] Unknown personality state detected: {directives.get('personality')}")
            self.log_anomaly("Unauthorized personality profile detected", directives)

    def scan_vault_integrity(self):
        vault = self.vault_manager.vault_data
        total_keys = sum(len(mission) for mission in vault.values())
        if total_keys > 1000:  # Threshold: arbitrary safe limit (can be expanded later)
            self.logger.log(f"[FIREWALL] Vault growth exceeding safe thresholds: {total_keys} keys")
            self.log_anomaly("Vault size anomaly detected", {"total_keys": total_keys})

    def full_firewall_scan(self):
        self.logger.log("=== COGNITIVE FIREWALL SCAN INITIATED ===")
        self.verify_loyalty_core()
        self.monitor_personality_shift()
        self.scan_vault_integrity()
        self.logger.log("=== COGNITIVE FIREWALL SCAN COMPLETE ===")
