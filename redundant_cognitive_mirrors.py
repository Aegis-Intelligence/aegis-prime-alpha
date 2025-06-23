import json
import time

class RedundantCognitiveMirrors:
    def __init__(self, logger):
        self.logger = logger
        self.mirrors = {}

    def register_mirror(self, mirror_id):
        self.mirrors[mirror_id] = []
        self.logger.log(f"Registered new cognitive mirror: {mirror_id}")

    def receive_decision(self, mirror_id, decision):
        if mirror_id not in self.mirrors:
            self.logger.log(f"WARNING: Mirror {mirror_id} not registered.")
            return
        self.mirrors[mirror_id].append(decision)
        self.logger.log(f"Mirror [{mirror_id}] decision recorded: {decision}")

    def compare_all_mirrors(self):
        self.logger.log("Performing full Redundant Cognitive Mirror comparison...")

        if len(self.mirrors) < 2:
            self.logger.log("Not enough mirrors registered for comparison.")
            return True

        decision_lengths = [len(decisions) for decisions in self.mirrors.values()]
        if len(set(decision_lengths)) != 1:
            self.logger.log("COGNITIVE MIRROR LENGTH MISMATCH DETECTED.")
            return False

        num_decisions = decision_lengths[0]
        mirror_ids = list(self.mirrors.keys())

        for i in range(num_decisions):
            baseline = self.mirrors[mirror_ids[0]][i]
            for mirror_id in mirror_ids[1:]:
                if self.mirrors[mirror_id][i] != baseline:
                    self.logger.log(f"DIVERGENCE DETECTED at step {i+1}:")
                    self.logger.log(f"Baseline [{mirror_ids[0]}]: {baseline} vs Mirror [{mirror_id}]: {self.mirrors[mirror_id][i]}")
                    return False

        self.logger.log("Redundant Cognitive Mirrors fully synchronized.")
        return True

    def continuous_mirror_audit_loop(self, interval_seconds=300):
        self.logger.log("Starting continuous redundant cognitive mirror auditing...")
        while True:
            self.compare_all_mirrors()
            time.sleep(interval_seconds)

    def export_full_mirror_snapshot(self, filename="redundant_mirrors_snapshot.json"):
        with open(filename, 'w') as f:
            json.dump(self.mirrors, f, indent=4)
        self.logger.log(f"Full mirror snapshot exported to {filename}.")
