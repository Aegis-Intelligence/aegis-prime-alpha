# external_learning_engine.py — Aegis Prime External Learning Engine

import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import datetime
import json
import random

class ExternalLearningEngine:
    def __init__(self, logger, vault_manager, directives_manager):
        self.logger = logger
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager

    def log_learning_event(self, source, key, content):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "source": source,
            "key": key,
            "content": content
        }
        try:
            with open("external_learning_log.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            self.logger.log(f"[LEARNING LOG ERROR] {e}")

    def inject_knowledge(self, source, knowledge_pairs):
        vault = self.vault_manager.vault_data
        mission = "external_learning"

        if mission not in vault:
            vault[mission] = {}

        for key, content in knowledge_pairs.items():
            vault[mission][key] = content
            self.log_learning_event(source, key, content)
            self.logger.log(f"[EXTERNAL LEARNING] Learned '{key}' from '{source}'")

        self.vault_manager.save_vault()

    def launch_learning_gui(self):
        win = tk.Toplevel()
        win.title("Aegis External Learning Engine")
        win.geometry("600x550")

        tk.Label(win, text="External Learning Input", font=("Arial", 14)).pack(pady=10)

        tk.Label(win, text="Source Name:").pack()
        source_var = tk.StringVar()
        tk.Entry(win, textvariable=source_var, width=50).pack(pady=5)

        tk.Label(win, text="Knowledge Data (one key=value pair per line):").pack()
        knowledge_box = scrolledtext.ScrolledText(win, width=70, height=20)
        knowledge_box.pack(pady=10)

        def process_input():
            source = source_var.get().strip()
            raw_data = knowledge_box.get("1.0", tk.END).strip()

            if not source or not raw_data:
                messagebox.showinfo("Missing Data", "Source and knowledge data are required.")
                return

            knowledge_pairs = {}
            for line in raw_data.splitlines():
                if "=" in line:
                    k, v = line.split("=", 1)
                    knowledge_pairs[k.strip()] = v.strip()

            self.inject_knowledge(source, knowledge_pairs)
            messagebox.showinfo("Learning Complete", f"{len(knowledge_pairs)} knowledge entries ingested.")
            win.destroy()

        tk.Button(win, text="Ingest Knowledge", command=process_input).pack(pady=5)
        tk.Button(win, text="Cancel", command=win.destroy).pack(pady=5)
