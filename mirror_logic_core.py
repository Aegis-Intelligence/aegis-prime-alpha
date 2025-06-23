import json
import time

class MirrorLogicCore:
    def __init__(self, logger):
        self.logger = logger
        self.primary_reasoning_log = []
        self.mirror_reasoning_log = []

    def receive_primary_decision(self, decision):
        self.logger.log(f"Primary Decision Received: {decision}")
        self.primary_reasoning_log.append(decision)

    def receive_mirror_decision(self, decision):
        self.logger.log(f"Mirror Decision Received: {decision}")
        self.mirror_reasoning_log.append(decision)

    def compare_reasoning_paths(self):
        self.logger.log("Performing Mirror Logic Comparison...")
        if len(self.primary_reasoning_log) != len(self.mirror_reasoning_log):
            self.logger.log("MIRROR LOGIC WARNING: Reasoning path length mismatch.")
            return False

        for i in range(len(self.primary_reasoning_log)):
            primary = self.primary_reasoning_log[i]
            mirror = self.mirror_reasoning_log[i]
            if primary != mirror:
                self.logger.log(f"MIRROR LOGIC DIVERGENCE DETECTED at step {i+1}:")
                self.logger.log(f"Primary: {primary} | Mirror: {mirror}")
                return False

        self.logger.log("Mirror Logic: Reasoning paths fully synchronized.")
        return True

    def continuous_mirror_supervision(self, interval_seconds=300):
        self.logger.log("Starting continuous Mirror Logic integrity supervision...")
        while True:
            self.compare_reasoning_paths()
            time.sleep(interval_seconds)

    def export_full_reasoning_logs(self, filename="mirror_logic_snapshot.json"):
        snapshot = {
            'primary': self.primary_reasoning_log,
            'mirror': self.mirror_reasoning_log
        }
        with open(filename, 'w') as f:
            json.dump(snapshot, f, indent=4)
        self.logger.log(f"Mirror Logic snapshot exported to {filename}.")
