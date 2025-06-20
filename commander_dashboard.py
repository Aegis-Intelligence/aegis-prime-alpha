# commander_dashboard.py — Aegis Prime Commander Dashboard Interface

import tkinter as tk
import datetime

class CommanderDashboard:
    def __init__(self, logger, vault_manager, directives_manager, firewall_module):
        self.logger = logger
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager
        self.firewall = firewall_module

    def refresh_dashboard(self, win, status_labels):
        directives = self.directives_manager.directives
        vault = self.vault_manager.vault_data
        total_keys = sum(len(mission) for mission in vault.values())

        status_labels['personality'].config(
            text=f"Personality: {directives.get('personality', 'UNKNOWN')}")
        status_labels['loyalty'].config(
            text=f"Loyalty: {directives.get('loyalty', 'UNKNOWN')}")
        status_labels['vault_keys'].config(
            text=f"Vault Keys: {total_keys}")
        status_labels['adaptation'].config(
            text=f"Memory Adaptation: {directives.get('memory_adaptation', 'UNKNOWN')}")

        self.logger.log("[DASHBOARD] Refreshed system status.")
        win.after(10000, lambda: self.refresh_dashboard(win, status_labels))  # Auto-refresh every 10 seconds

    def run_firewall_check(self):
        self.firewall.full_firewall_scan()

    def launch_dashboard(self):
        win = tk.Toplevel()
        win.title("Aegis Prime Commander Dashboard")
        win.geometry("500x400")

        tk.Label(win, text="Commander Sovereign Control Panel", font=("Arial", 14)).pack(pady=10)

        status_labels = {}
        status_labels['personality'] = tk.Label(win, text="", font=("Arial", 12))
        status_labels['personality'].pack(pady=5)
        status_labels['loyalty'] = tk.Label(win, text="", font=("Arial", 12))
        status_labels['loyalty'].pack(pady=5)
        status_labels['vault_keys'] = tk.Label(win, text="", font=("Arial", 12))
        status_labels['vault_keys'].pack(pady=5)
        status_labels['adaptation'] = tk.Label(win, text="", font=("Arial", 12))
        status_labels['adaptation'].pack(pady=5)

        tk.Button(win, text="Run Cognitive Firewall Check", command=self.run_firewall_check).pack(pady=20)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

        self.refresh_dashboard(win, status_labels)
        win.mainloop()
