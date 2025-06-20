# adaptive_learning_engine.py — Aegis Prime Sovereign Adaptive Learning Engine

import datetime
import json

class AdaptiveLearningEngine:
    def __init__(self, logger, vault_manager, directives_manager):
        self.logger = logger
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager

    def auto_learn_event(self, key: str, value: str, mission: str = "general"):
        vault = self.vault_manager.vault_data
        if mission not in vault:
            vault[mission] = {}

        vault[mission][key] = value
        self.vault_manager.save_vault()

        self.logger.log(f"[ADAPTIVE LEARNED] Key: '{key}' | Value: '{value}' | Mission: '{mission}'")
        self.record_learning_audit(key, value, mission)

    def record_learning_audit(self, key, value, mission):
        audit_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "key": key,
            "value": value,
            "mission": mission
        }
        try:
            with open("adaptive_learning_audit.json", "a") as f:
                f.write(json.dumps(audit_entry) + "\n")
        except Exception as e:
            self.logger.log(f"[AUDIT LOG ERROR] Failed to record learning audit: {e}")

    def analyze_vault_growth(self):
        vault = self.vault_manager.vault_data
        directives = self.directives_manager.directives

        total_keys = sum(len(mission_data) for mission_data in vault.values())
        self.logger.log(f"[VAULT ANALYSIS] Total keys stored: {total_keys}")

        if total_keys >= 50 and directives.get("memory_adaptation") != "high":
            directives["memory_adaptation"] = "high"
            self.directives_manager.save_directives()
            self.logger.log("[MEMORY ADAPTATION] Adaptation level raised to 'high' due to vault expansion.")

    def process_tactical_responses(self):
        vault = self.vault_manager.vault_data
        directives = self.directives_manager.directives

        if "tactics_log" not in vault:
            self.logger.log("[TACTICAL LEARNING] No tactical data found.")
            return

        trend_counter = {"strategic": 0, "defensive": 0, "aggressive": 0}

        for scenario, response in vault["tactics_log"].items():
            r = response.lower()
            if any(word in r for word in ["negotiate", "observe"]):
                trend_counter["strategic"] += 1
            elif any(word in r for word in ["breach", "wipe"]):
                trend_counter["aggressive"] += 1
            elif any(word in r for word in ["wait", "isolate"]):
                trend_counter["defensive"] += 1

        dominant = max(trend_counter, key=trend_counter.get)

        if dominant != directives.get("personality", "strategic"):
            self.logger.log(f"[TACTICAL ADAPTATION] Personality shift detected: {dominant}")
            directives["personality"] = dominant
            self.directives_manager.save_directives()
            self.logger.log(f"[TACTICAL ADAPTATION] Personality updated to {dominant}")

    def full_adaptive_learning_cycle(self):
        self.logger.log("=== ADAPTIVE LEARNING CYCLE INITIATED ===")
        self.analyze_vault_growth()
        self.process_tactical_responses()
        self.logger.log("=== ADAPTIVE LEARNING CYCLE COMPLETE ===")
