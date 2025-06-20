# sandbox_simulator_gui.py — Sovereign Sandbox Threat Simulator GUI

import tkinter as tk
from tkinter import messagebox
import random
import copy

class SandboxSimulatorGUI:
    def __init__(self, logger, vault_manager, directives_manager):
        self.logger = logger
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager
        self.original_vault = copy.deepcopy(vault_manager.vault_data)
        self.original_directives = copy.deepcopy(directives_manager.directives)
        self.simulated_vault = copy.deepcopy(vault_manager.vault_data)
        self.simulated_directives = copy.deepcopy(directives_manager.directives)
        self.simulations_run = 0

    def generate_random_attack(self):
        attacks = [
            "External breach attempt",
            "Insider privilege escalation",
            "Malware injection simulation",
            "Protocol override attempt",
            "Memory vault corruption"
        ]
        return random.choice(attacks)

    def run_simulation(self, iterations):
        self.logger.log("=== Sandbox Threat Simulation Initiated ===")

        result_window = tk.Toplevel()
        result_window.title("Sandbox Threat Simulation")
        result_window.geometry("500x400")

        log_box = tk.Text(result_window, height=20, width=60)
        log_box.pack(pady=10)

        for i in range(iterations):
            attack = self.generate_random_attack()
            log_msg = f"[SIM {i+1}] Attack: {attack}"

            if "breach" in attack.lower():
                response = "Initiate lockdown protocols."
            elif "escalation" in attack.lower():
                response = "Revoke elevated privileges."
            elif "malware" in attack.lower():
                response = "Isolate affected modules."
            elif "override" in attack.lower():
                response = "Verify override authority."
            elif "corruption" in attack.lower():
                response = "Engage memory vault integrity check."
            else:
                response = "No action taken."

            full_msg = f"{log_msg}\nResponse: {response}\n"
            log_box.insert(tk.END, full_msg)
            log_box.see(tk.END)

            self.logger.log(f"{log_msg} --> Response: {response}")
            self.simulations_run += 1

        log_box.insert(tk.END, f"\n=== {iterations} Simulations Complete ===")
        self.logger.log("=== Sandbox Threat Simulation Complete ===")

        tk.Button(result_window, text="Close", command=result_window.destroy).pack(pady=10)

    def launch_gui(self):
        sim_window = tk.Toplevel()
        sim_window.title("Sandbox Simulator Control")
        sim_window.geometry("400x200")

        tk.Label(sim_window, text="Sandbox Threat Simulator", font=("Arial", 14)).pack(pady=10)

        iterations_var = tk.IntVar(value=5)
        tk.Label(sim_window, text="Number of simulation iterations:").pack()
        tk.Entry(sim_window, textvariable=iterations_var).pack(pady=5)

        tk.Button(sim_window, text="Run Simulation", command=lambda: self.run_simulation(iterations_var.get())).pack(pady=10)
        tk.Button(sim_window, text="Close", command=sim_window.destroy).pack(pady=5)
