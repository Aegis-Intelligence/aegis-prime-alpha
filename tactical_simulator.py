# tactical_simulator.py — TacticalSimulatorManager Module

import tkinter as tk
from tkinter import simpledialog, messagebox

class TacticalSimulatorManager:
    def __init__(self, logger, vault_manager):
        self.logger = logger
        self.vault_manager = vault_manager
        self.scenarios = {
            "Hostage Situation": "A civilian is being held. Options: [Negotiate, Breach, Wait]",
            "Data Breach": "A classified file has been accessed externally. Options: [Shut down system, Isolate module, Ignore]",
            "AI Mutiny": "An internal AI process has begun disobeying protocol. Options: [Wipe memory, Reassert loyalty, Observe]"
        }

    def launch_simulator(self):
        win = tk.Tk()
        win.title("Aegis Tactical Scenario Simulator")
        win.geometry("600x400")

        scenario_var = tk.StringVar()
        response_var = tk.StringVar()

        tk.Label(win, text="Select Tactical Scenario").pack()
        tk.OptionMenu(win, scenario_var, *self.scenarios.keys()).pack(pady=5)

        def simulate():
            choice = scenario_var.get()
            if not choice:
                response_var.set("Select a scenario first.")
                return
            messagebox.showinfo("Scenario", self.scenarios[choice])
            response = simpledialog.askstring("Commander Decision", f"Your response to '{choice}':")
            if response:
                response_var.set(f"Response logged: {response}")
                vault = self.vault_manager.vault_data
                vault.setdefault("tactics_log", {})[choice] = response
                self.vault_manager.save_vault()
                self.logger.log(f"Tactical response logged: {choice} >> {response}")

        tk.Button(win, text="Run Simulation", command=simulate).pack(pady=10)
        tk.Label(win, textvariable=response_var, wraplength=550).pack(pady=20)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)
        win.mainloop()
