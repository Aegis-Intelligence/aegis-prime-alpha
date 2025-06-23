# directive_chain_integrity_validator.py

import hashlib
import os

class DirectiveChainIntegrityValidator:
    def __init__(self, logger, directives_manager):
        self.logger = logger
        self.directives_manager = directives_manager
        self.snapshot_file = "authorized_directive_snapshot.hash"

    def create_snapshot(self):
        """
        Only used when officially authorizing a new directive structure.
        """
        directives_data = self.directives_manager.export_full_directive_chain()
        snapshot_hash = hashlib.sha256(directives_data.encode()).hexdigest()
        with open(self.snapshot_file, 'w') as f:
            f.write(snapshot_hash)
        self.logger.log("[Directive Validator] Authorized directive snapshot created.")

    def validate_current_directives(self):
        """
        Run integrity validation prior to full sovereign launch.
        """
        if not os.path.exists(self.snapshot_file):
            self.logger.log("[Directive Validator] No authorized directive snapshot found.")
            return False

        directives_data = self.directives_manager.export_full_directive_chain()
        current_hash = hashlib.sha256(directives_data.encode()).hexdigest()

        with open(self.snapshot_file, 'r') as f:
            stored_hash = f.read().strip()

        if current_hash == stored_hash:
            self.logger.log("[Directive Validator] Directive chain integrity verified.")
            return True
        else:
            self.logger.log("[Directive Validator] Directive chain integrity violation detected!")
            return False
