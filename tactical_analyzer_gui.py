# tactical_analyzer_gui.py — Sovereign Tactical Analyzer Module

import tkinter as tk
from tkinter import messagebox
import json

class TacticalAnalyzerGUI:
    def __init__(self, logger, vault_manager, directives_manager):
        self.logger = logger
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager

    def analyze_tactics(self):
        vault = self.vault_manager.vault_data
        directives = self.directives_manager.directives

        if "tactics_log" not in vault or not vault["tactics_log"]:
            self.logger.log("No tactical logs to analyze.")
            messagebox.showinfo("Tactical Analyzer", "No tactical log data available.")
            return

        trend_counter = {"strategic": 0, "defensive": 0, "aggressive": 0}

        for scenario, response in vault["tactics_log"].items():
            r = response.lower()
            if any(word in r for word in ["negotiate", "observe"]):
                trend_counter["strategic"] += 1
            elif any(word in r for word in ["breach", "wipe"]):
                trend_counter["aggressive"] += 1
            elif any(word in r for word in ["wait", "isolate"]):
                trend_counter["defensive"] += 1

        dominant = max(trend_counter, key=trend_counter.get)

        # Display results in GUI
        result_window = tk.Toplevel()
        result_window.title("Tactical Analysis Results")
        result_window.geometry("400x300")

        tk.Label(result_window, text="Tactical Trend Analysis", font=("Arial", 14)).pack(pady=10)
        tk.Label(result_window, text=f"Strategic: {trend_counter['strategic']}").pack()
        tk.Label(result_window, text=f"Defensive: {trend_counter['defensive']}").pack()
        tk.Label(result_window, text=f"Aggressive: {trend_counter['aggressive']}").pack()

        tk.Label(result_window, text=f"\nDominant Trend: {dominant.upper()}", font=("Arial", 12, "bold")).pack(pady=10)

        current_personality = directives.get("personality", "strategic")
        if dominant != current_personality:
            def apply_update():
                directives["personality"] = dominant
                self.directives_manager.save_directives()
                self.logger.log(f"Personality updated to {dominant} based on tactical trends.")
                messagebox.showinfo("Update Applied", f"Personality updated to {dominant.upper()}.")
                result_window.destroy()

            tk.Label(result_window, text=f"Current Personality: {current_personality.upper()}").pack(pady=5)
            tk.Button(result_window, text=f"Apply new personality: {dominant.upper()}", command=apply_update).pack(pady=10)

        tk.Button(result_window, text="Close", command=result_window.destroy).pack(pady=10)

        self.logger.log(f"Tactical analysis complete. Dominant: {dominant}")

