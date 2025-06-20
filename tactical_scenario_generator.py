# tactical_scenario_generator.py — Aegis Prime Tactical Scenario Generator AI

import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import datetime
import json
import random

class TacticalScenarioGenerator:
    def __init__(self, logger):
        self.logger = logger
        self.generated_log = "generated_scenarios_log.json"

    def log_generated_scenario(self, scenario):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "scenario": scenario
        }
        try:
            with open(self.generated_log, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            self.logger.log(f"[SCENARIO GENERATOR LOG ERROR] {e}")

    def generate_scenario(self, difficulty="normal"):
        # Core scenario elements
        threat_types = [
            "Cyber attack", "AI insurrection", "Data breach", "Espionage operation", "Infrastructure sabotage",
            "Civil unrest", "Rogue nation aggression", "Critical infrastructure failure", "Biological threat", "Space asset compromise"
        ]

        adversary_profiles = [
            "Rogue AI collective", "Foreign intelligence agency", "Internal whistleblower group",
            "Dissident faction", "Unidentified external entity", "Hostile corporate syndicate"
        ]

        possible_objectives = [
            "Extract classified data", "Destabilize governance", "Seize critical infrastructure",
            "Undermine leadership authority", "Neutralize AI sovereignty", "Trigger diplomatic crisis"
        ]

        # Adjust difficulty weight
        if difficulty == "easy":
            complexity = 1
        elif difficulty == "hard":
            complexity = 3
        else:  # normal
            complexity = 2

        # Randomized scenario generation
        threat = random.choice(threat_types)
        adversary = random.choice(adversary_profiles)
        objective = random.choice(possible_objectives)
        complications = random.sample(possible_objectives, complexity)

        scenario = {
            "threat": threat,
            "adversary": adversary,
            "primary_objective": objective,
            "complications": complications
        }

        self.log_generated_scenario(scenario)
        return scenario

    def launch_scenario_gui(self):
        win = tk.Toplevel()
        win.title("Tactical Scenario Generator AI")
        win.geometry("600x500")

        difficulty_var = tk.StringVar(value="normal")

        tk.Label(win, text="Generate New Tactical Scenario", font=("Arial", 14)).pack(pady=10)
        tk.Label(win, text="Select Difficulty Level:").pack()
        tk.OptionMenu(win, difficulty_var, "easy", "normal", "hard").pack(pady=5)

        log_box = scrolledtext.ScrolledText(win, width=70, height=20, state=tk.DISABLED)
        log_box.pack(pady=10)

        def generate_and_display():
            scenario = self.generate_scenario(difficulty_var.get())
            log_box.config(state=tk.NORMAL)
            log_box.insert(tk.END, f"\n=== New Tactical Scenario ===\n")
            log_box.insert(tk.END, f"Threat: {scenario['threat']}\n")
            log_box.insert(tk.END, f"Adversary: {scenario['adversary']}\n")
            log_box.insert(tk.END, f"Primary Objective: {scenario['primary_objective']}\n")
            log_box.insert(tk.END, f"Complications: {', '.join(scenario['complications'])}\n")
            log_box.insert(tk.END, "-"*50 + "\n")
            log_box.config(state=tk.DISABLED)
            log_box.see(tk.END)

            self.logger.log(f"[TACTICAL SCENARIO GENERATED] {scenario}")

        tk.Button(win, text="Generate Scenario", command=generate_and_display).pack(pady=10)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)
