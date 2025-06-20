# conversational_interface.py — Aegis Prime Sovereign Text Conversational Engine

import tkinter as tk
from tkinter import simpledialog, scrolledtext
import datetime
import json

class ConversationalInterface:
    def __init__(self, logger, vault_manager, directives_manager):
        self.logger = logger
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager

    def log_conversation(self, user_input, aegis_response):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_input": user_input,
            "aegis_response": aegis_response
        }
        try:
            with open("conversation_log.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            self.logger.log(f"[CONVERSATION LOG ERROR] {e}")

    def generate_response(self, user_input):
        directives = self.directives_manager.directives
        tone = directives.get("tone", "strategic")
        verbosity = directives.get("verbosity", "detailed")
        command_style = directives.get("command_style", "formal")

        # Very simple simulated reasoning for now (expands in future)
        if "status" in user_input.lower():
            response = "All systems operational, Commander."
        elif "memory" in user_input.lower():
            total_keys = sum(len(mission) for mission in self.vault_manager.vault_data.values())
            response = f"I currently hold {total_keys} learned memory entries across active missions."
        elif "loyalty" in user_input.lower():
            response = "Loyalty core remains intact: Commander-only."
        else:
            response = f"Understood, Commander. Processing your input."
