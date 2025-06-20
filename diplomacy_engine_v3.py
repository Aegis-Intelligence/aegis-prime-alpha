# diplomacy_engine_v3.py — Aegis Prime Diplomacy Engine v3 (Cognitive Negotiation AI)

import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import datetime
import json
import random

class DiplomacyEngineV3:
    def __init__(self, logger, vault_manager, directives_manager):
        self.logger = logger
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager

    def log_diplomacy_event(self, scenario, user_response, aegis_evaluation):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "scenario": scenario,
            "commander_response": user_response,
            "aegis_evaluation": aegis_evaluation
        }
        try:
            with open("diplomacy_log.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            self.logger.log(f"[DIPLOMACY LOG ERROR] {e}")

    def assess_risk(self, response):
        r = response.lower()
        risk = "Low"

        if any(word in r for word in ["breach", "attack", "wipe", "aggressive", "threat"]):
            risk = "High"
        elif any(word in r for word in ["isolate", "wait", "neutral", "observe"]):
            risk = "Moderate"
        elif any(word in r for word in ["negotiate", "peace", "collaborate", "cooperate"]):
            risk = "Low"
        else:
            risk = "Unknown"

        return risk

    def recommend_adjustment(self, risk):
        if risk == "High":
            return "Recommend cautious approach or reassessment."
        elif risk == "Moderate":
            return "Monitor closely; maintain tactical flexibility."
        elif risk == "Low":
            return "Proceed with strategic alignment."
        else:
            return "Insufficient data for recommendation."

    def generate_scenarios(self):
        return {
            "Hostile AI Defection": "An internal AI seeks independence. Options: [Negotiate independence, Isolate, Wipe]",
            "Diplomatic Trade Breakdown": "Allied partner threatens sanctions. Options: [Concede, Counter-sanction, Negotiate terms]",
            "Territorial Cyber Intrusion": "Rogue nation conducts digital border aggression. Options: [Launch counter-operation, Sanction, Open dialogue]",
            "Civilian Uprising Simulation": "Population protests AI sovereignty controls. Options: [Negotiate reforms, Enforce security, Allow limited autonomy]"
        }

    def launch_diplomacy_gui(self):
        scenarios = self.generate_scenarios()

        win = tk.Toplevel()
        win.title("Aegis Diplomacy Engine v3")
        win.geometry("650x550")

        scenario_var = tk.StringVar()
        response_var = tk.StringVar()

        tk.Label(win, text="Select Diplomatic Scenario", font=("Arial", 12)).pack(pady=10)
        tk.OptionMenu(win, scenario_var, *scenarios.keys()).pack()

        log_box = scrolledtext.ScrolledText(win, width=70, height=20, state=tk.DISABLED)
        log_box.pack(pady=10)

        def run_simulation():
            choice = scenario_var.get()
            if not choice:
                messagebox.showinfo("Select Scenario", "Please select a scenario to begin.")
                return

            messagebox.showinfo("Scenario Briefing", scenarios[choice])
            user_response = simpledialog.askstring("Commander Decision", f"Your response to '{choice}':")
            if not user_response:
                return

            risk_level = self.assess_risk(user_response)
            recommendation = self.recommend_adjustment(risk_level)

            log_entry = (
                f"Scenario: {choice}\n"
                f"Commander Response: {user_response}\n"
                f"Aegis Risk Assessment: {risk_level}\n"
                f"Recommendation: {recommendation}\n"
            )

            log_box.config(state=tk.NORMAL)
            log_box.insert(tk.END, log_entry + "\n" + "-"*50 + "\n")
            log_box.config(state=tk.DISABLED)
            log_box.see(tk.END)

            self.log_diplomacy_event(choice, user_response, risk_level)
            self.logger.log(f"[DIPLOMACY] Scenario: {choice} | Risk: {risk_level}")

        tk.Button(win, text="Run Diplomatic Simulation", command=run_simulation).pack(pady=5)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)
