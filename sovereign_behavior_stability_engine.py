import time
import json

class SovereignBehaviorStabilityEngine:
    def __init__(self, logger, directives_manager):
        self.logger = logger
        self.directives_manager = directives_manager

        # Stability baseline profile (Commander controlled)
        self.personality_profile = {
            "empathy_level": 0.75,
            "assertiveness": 0.80,
            "tactical_reserve": 0.85,
            "emotional_dampening": 0.90,
            "sovereign_risk_tolerance": 0.70
        }

        # Deviation logs
        self.deviation_logs = []

    # === Behavior Monitoring ===

    def monitor_behavior_deviation(self, current_profile):
        deviation_detected = False
        deviations = {}

        for trait, baseline in self.personality_profile.items():
            current_value = current_profile.get(trait, baseline)
            delta = abs(current_value - baseline)

            if delta > 0.15:  # Commander-defined deviation threshold
                deviations[trait] = delta
                deviation_detected = True

        if deviation_detected:
            self.logger.log(f"Behavior deviation detected: {deviations}")
            self.log_deviation_event(deviations)
            self.enforce_correction(current_profile, deviations)
        else:
            self.logger.log("Behavior profile stable.")

    # === Enforcement Logic ===

    def enforce_correction(self, current_profile, deviations):
        self.logger.log("Engaging sovereign correction protocols.")
        for trait, delta in deviations.items():
            corrected_value = self.personality_profile[trait]
            current_profile[trait] = corrected_value
            self.logger.log(f"Corrected {trait} -> {corrected_value}")

        self.logger.log("Sovereign behavior correction completed.")

    # === Deviation Logging ===

    def log_deviation_event(self, deviations):
        event = {
            "timestamp": time.time(),
            "deviations": deviations,
            "directives_snapshot": self.directives_manager.get_active_directives()
        }
        self.deviation_logs.append(event)

    def export_deviation_logs(self, filename="behavior_deviation_logs.json"):
        with open(filename, 'w') as f:
            json.dump(self.deviation_logs, f, indent=4)
        self.logger.log(f"Deviation logs exported to {filename}.")

    # === Commander Controls ===

    def update_personality_profile(self, trait, new_value):
        if trait in self.personality_profile:
            self.personality_profile[trait] = new_value
            self.logger.log(f"Personality trait '{trait}' updated to {new_value}.")
