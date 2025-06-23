import time
import json
import hashlib

class ReasoningDriftDetector:
    def __init__(self, logger):
        self.logger = logger
        self.reference_profiles = {}  # Sovereign reference reasoning hashes
        self.drift_log = []

    def register_reference_profile(self, module_name, reasoning_output):
        reasoning_hash = hashlib.sha256(reasoning_output.encode('utf-8')).hexdigest()
        self.reference_profiles[module_name] = reasoning_hash
        self.logger.log(f"Reference reasoning profile registered for: {module_name}")

    def monitor_reasoning_consistency(self, module_name, new_reasoning_output):
        if module_name not in self.reference_profiles:
            self.logger.log(f"No reference profile found for module: {module_name}.")
            return True

        new_hash = hashlib.sha256(new_reasoning_output.encode('utf-8')).hexdigest()
        reference_hash = self.reference_profiles[module_name]

        if new_hash != reference_hash:
            drift_entry = {
                "timestamp": time.time(),
                "module": module_name,
                "reference_hash": reference_hash,
                "new_hash": new_hash
            }
            self.drift_log.append(drift_entry)
            self.logger.log(f"REASONING DRIFT DETECTED in module: {module_name}")
            return False
        else:
            self.logger.log(f"No reasoning drift detected for: {module_name}")
            return True

    def export_drift_log(self, filename="reasoning_drift_log.json"):
        with open(filename, 'w') as f:
            json.dump(self.drift_log, f, indent=4)
        self.logger.log(f"Drift log exported to {filename}.")
