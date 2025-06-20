# directives_manager.py — Aegis Prime Sovereign Directives Manager

import os
import json
import tkinter as tk
from tkinter import simpledialog, messagebox

DIRECTIVES_FILE = "aegis_directives.json"
DIRECTIVES_BACKUP_FILE = "aegis_directives_backup.json"

class DirectivesManager:
    def __init__(self, logger):
        self.logger = logger
        self.directives = {}
        self.load_directives()

    def load_directives(self):
        try:
            if not os.path.exists(DIRECTIVES_FILE):
                raise FileNotFoundError("Directive file missing.")
            with open(DIRECTIVES_FILE, "r") as f:
                self.directives = json.load(f)

            with open(DIRECTIVES_BACKUP_FILE, "w") as backup:
                json.dump(self.directives, backup, indent=2)

            self.logger.log("Directives loaded successfully.")
        except Exception as e:
            self.logger.log(f"Failed to load directives: {e}")

            # Attempt recovery from backup
            if os.path.exists(DIRECTIVES_BACKUP_FILE):
                self.logger.log("Restoring directives from backup...")
                with open(DIRECTIVES_BACKUP_FILE, "r") as f:
                    self.directives = json.load(f)
                self.save_directives()
            else:
                self.logger.log("No backup found. Creating default directives.")
                self.directives = self.get_default_directives()
                self.save_directives()

    def get_default_directives(self):
        return {
            "personality": "strategic",
            "loyalty": "Commander-only",
            "ambient_mode": "off",
            "memory_adaptation": "enabled",
            "override": "",
            "voice_lock_hash": "",
            "tone": "strategic",
            "verbosity": "detailed",
            "command_style": "formal"
        }

    def save_directives(self):
        self.directives["loyalty"] = "Commander-only"  # Enforce immutable loyalty
        with open(DIRECTIVES_FILE, "w") as f:
            json.dump(self.directives, f, indent=2)
        with open(DIRECTIVES_BACKUP_FILE, "w") as backup:
            json.dump(self.directives, backup, indent=2)
        self.logger.log("Directives updated.")

    def launch_persona_sculptor(self):
        win = tk.Toplevel()
        win.title("Aegis Persona Sculptor")
        win.geometry("400x400")

        tone_var = tk.StringVar(value=self.directives.get("tone", "strategic"))
        verbosity_var = tk.StringVar(value=self.directives.get("verbosity", "detailed"))
        command_style_var = tk.StringVar(value=self.directives.get("command_style", "formal"))

        tk.Label(win, text="Tone").pack()
        tk.OptionMenu(win, tone_var, "strategic", "warm", "cold", "neutral").pack()

        tk.Label(win, text="Verbosity").pack()
        tk.OptionMenu(win, verbosity_var, "minimal", "detailed", "expressive").pack()

        tk.Label(win, text="Command Style").pack()
        tk.OptionMenu(win, command_style_var, "formal", "informal", "tactical").pack()

        def save_persona():
            self.directives["tone"] = tone_var.get()
            self.directives["verbosity"] = verbosity_var.get()
            self.directives["command_style"] = command_style_var.get()
            self.save_directives()
            messagebox.showinfo("Saved", "Persona traits updated.")
            self.logger.log(f"Persona updated: Tone={tone_var.get()}, Verbosity={verbosity_var.get()}, Style={command_style_var.get()}")

        tk.Button(win, text="Save Persona", command=save_persona).pack(pady=10)
        tk.Button(win, text="Close", command=win.destroy).pack()

        self.logger.log("Persona Sculptor interface opened.")
