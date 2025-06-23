import hashlib
import os
import json
import time

class SovereignCodeValidator:
    def __init__(self, logger, watch_modules, hash_file='trusted_hashes.json'):
        self.logger = logger
        self.watch_modules = watch_modules
        self.hash_file = hash_file
        self.trusted_hashes = {}

        if not os.path.exists(self.hash_file):
            self.logger.log("No trusted hashes found. Generating initial trusted hashes.")
            self.generate_trusted_hashes()
        else:
            self.load_trusted_hashes()

    def generate_file_hash(self, file_path):
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def generate_trusted_hashes(self):
        self.trusted_hashes = {}
        for module in self.watch_modules:
            if os.path.exists(module):
                self.trusted_hashes[module] = self.generate_file_hash(module)
            else:
                self.logger.log(f"WARNING: Module file not found during hash generation: {module}")
        with open(self.hash_file, 'w') as f:
            json.dump(self.trusted_hashes, f, indent=4)
        self.logger.log("Trusted hashes generated and stored.")

    def load_trusted_hashes(self):
        with open(self.hash_file, 'r') as f:
            self.trusted_hashes = json.load(f)
        self.logger.log("Trusted hashes loaded from storage.")

    def validate_code_integrity(self):
        for module, trusted_hash in self.trusted_hashes.items():
            if os.path.exists(module):
                current_hash = self.generate_file_hash(module)
                if current_hash != trusted_hash:
                    self.logger.log(f"CODE INTEGRITY VIOLATION DETECTED: {module}")
                    return False
            else:
                self.logger.log(f"WARNING: Module file missing during integrity check: {module}")
                return False
        self.logger.log("All modules passed integrity verification.")
        return True

    def continuous_validation_loop(self, interval_seconds=300):
        self.logger.log("Starting continuous sovereign code integrity monitoring...")
        while True:
            if not self.validate_code_integrity():
                self.logger.log("SOVEREIGN LOCKDOWN ENGAGED.")
                # Future: Trigger full system lockdown sequence here
                break
            time.sleep(interval_seconds)
