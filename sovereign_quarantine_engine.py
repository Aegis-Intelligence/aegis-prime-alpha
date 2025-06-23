import json
import time
import hashlib

class SovereignQuarantineEngine:
    def __init__(self, logger, mirror_logic, redundant_mirrors, cognitive_firewall):
        self.logger = logger
        self.mirror_logic = mirror_logic
        self.redundant_mirrors = redundant_mirrors
        self.cognitive_firewall = cognitive_firewall
        self.quarantine_buffer = []
        self.accepted_data_log = []
        self.rejected_data_log = []

    def quarantine_external_data(self, source_url, raw_data):
        timestamp = time.time()
        data_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
        quarantine_entry = {
            "timestamp": timestamp,
            "source_url": source_url,
            "data_hash": data_hash,
            "content": raw_data
        }
        self.logger.log(f"Incoming data quarantined from: {source_url}")
        self.quarantine_buffer.append(quarantine_entry)

    def evaluate_quarantine_buffer(self):
        self.logger.log("Starting quarantine buffer evaluation...")

        for entry in list(self.quarantine_buffer):  # Iterate safely over a copy
            data = entry['content']

            # 1️⃣ Firewall Scan
            if not self.cognitive_firewall.evaluate_data_content(data):
                self.logger.log(f"Data rejected by cognitive firewall from: {entry['source_url']}")
                self.rejected_data_log.append(entry)
                self.quarantine_buffer.remove(entry)
                continue

            # 2️⃣ Mirror Logic Validation
            primary_decision = f"ACCEPTED_CONTENT:{entry['data_hash']}"
            mirror_decision = f"ACCEPTED_CONTENT:{entry['data_hash']}"  # For this demo, simulate match

            self.mirror_logic.receive_primary_decision(primary_decision)
            self.mirror_logic.receive_mirror_decision(mirror_decision)

            if not self.mirror_logic.compare_reasoning_paths():
                self.logger.log(f"Mirror divergence detected during quarantine evaluation for {entry['source_url']}.")
                self.rejected_data_log.append(entry)
                self.quarantine_buffer.remove(entry)
                continue

            # 3️⃣ Redundant Mirror Consensus (optional escalation)
            self.redundant_mirrors.receive_decision("primary_chain", primary_decision)
            self.redundant_mirrors.receive_decision("mirror_chain", mirror_decision)
            self.redundant_mirrors.receive_decision("alternate_chain_1", primary_decision)
            self.redundant_mirrors.receive_decision("alternate_chain_2", primary_decision)

            if not self.redundant_mirrors.compare_all_mirrors():
                self.logger.log(f"Redundant cognitive mirror divergence detected for {entry['source_url']}.")
                self.rejected_data_log.append(entry)
                self.quarantine_buffer.remove(entry)
                continue

            # 4️⃣ If fully validated — accept into cognitive memory ingestion
            self.logger.log(f"External data fully accepted into sovereign ingestion: {entry['source_url']}")
            self.accepted_data_log.append(entry)
            self.quarantine_buffer.remove(entry)

    def export_quarantine_logs(self):
        with open("accepted_quarantine_data.json", "w") as f:
            json.dump(self.accepted_data_log, f, indent=4)
        with open("rejected_quarantine_data.json", "w") as f:
            json.dump(self.rejected_data_log, f, indent=4)
        self.logger.log("Quarantine evaluation logs exported.")
