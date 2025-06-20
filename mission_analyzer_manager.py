# mission_analyzer_manager.py — Aegis Prime Mission Analyzer Manager

class MissionAnalyzerManager:
    def __init__(self, logger, vault_manager, directives_manager):
        self.logger = logger
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager

    def analyze_tactics(self):
        vault = self.vault_manager.vault_data
        directives = self.directives_manager.directives

        if "tactics_log" not in vault:
            self.logger.log("No tactical logs to analyze.")
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
        self.logger.log(f"Tactical trend analysis complete: Dominant = {dominant}")

        if dominant != directives.get("personality", "strategic"):
            self.logger.log(f"Personality shift detected: {directives.get('personality')} -> {dominant}")
            directives["personality"] = dominant
            self.directives_manager.save_directives()
            self.logger.log("Personality updated based on tactical trend analysis.")
