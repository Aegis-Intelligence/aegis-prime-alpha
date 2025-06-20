# directive_manager.py — DirectiveHierarchyManager Module

import os
import json
from constants import DIRECTIVES_FILE, DIRECTIVES_BACKUP_FILE

class DirectiveHierarchyManager:
    def __init__(self, logger):
        self.logger = logger
        self.directives = {}

    def load_directives(self):
        try:
            if not os.path.exists(DIRECTIVES_FILE):
                raise FileNotFoundError("Directive file missing.")
            with open(DIRECTIVES_FILE, "r") as f:
                self.directives = json.load(f)
            with open(DIRECTIVES_BACKUP_FILE, "w") as backup:
                json.dump(self.directives, backup, indent=2)
            self.logger.log("Directives loaded successfully.")
            return self.directives
        except Exception as e:
            self.logger.log(f"Failed to load directives: {e}")
            if os.path.exists(DIRECTIVES_BACKUP_FILE):
                self.logger.log("Restoring from backup...")
                with open(DIRECTIVES_BACKUP_FILE, "r") as f:
                    self.directives = json.load(f)
                with open(DIRECTIVES_FILE, "w") as out:
                    json.dump(self.directives, out, indent=2)
                return self.directives
            else:
                self.logger.log("No backup found. Creating default directives.")
                self.directives = {
                    "personality": "strategic",
                    "loyalty": "Commander-only",
                    "ambient_mode": "off",
                    "memory_adaptation": "enabled",
                    "override": "",
                    "voice_lock_hash": ""
                }
                self.save_directives()
                return self.directives

    def save_directives(self):
        self.directives["loyalty"] = "Commander-only"
        with open(DIRECTIVES_FILE, "w") as f:
            json.dump(self.directives, f, indent=2)
        self.logger.log("Directives updated.")
