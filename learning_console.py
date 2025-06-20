# learning_console.py — LearningConsoleManager Module

import tkinter as tk
from tkinter import simpledialog

class LearningConsoleManager:
    def __init__(self, logger, vault_manager):
        self.logger = logger
        self.vault_manager = vault_manager

    def launch_learning_console(self):
        win = tk.Tk()
        win.title("Aegis Learning Console")
        win.geometry("500x400")

        key_var = tk.StringVar()
        value_var = tk.StringVar()
        mission_var = tk.StringVar(value="general")
        result_var = tk.StringVar()

        tk.Label(win, text="Key").pack()
        tk.Entry(win, textvariable=key_var).pack()
        tk.Label(win, text="Value").pack()
        tk.Entry(win, textvariable=value_var).pack()
        tk.Label(win, text="Mission").pack()
        tk.Entry(win, textvariable=mission_var).pack()

        def remember():
            k, v = key_var.get(), value_var.get()
            if k and v:
                self.vault_manager.vault_data.setdefault(mission_var.get(), {})[k] = v
                self.vault_manager.save_vault()
                result_var.set("Memory updated.")
                self.logger.log(f"Memory updated: {mission_var.get()} → {k}: {v}")

        def recall():
            k = key_var.get()
            v = self.vault_manager.vault_data.get(mission_var.get(), {}).get(k, "[Not Found]")
            result_var.set(v)

        def forget():
            k = key_var.get()
            if k in self.vault_manager.vault_data.get(mission_var.get(), {}):
                del self.vault_manager.vault_data[mission_var.get()][k]
                if not self.vault_manager.vault_data[mission_var.get()]:
                    del self.vault_manager.vault_data[mission_var.get()]
                self.vault_manager.save_vault()
                result_var.set("Entry removed.")
                self.logger.log(f"Entry removed: {mission_var.get()} → {k}")

        tk.Button(win, text="Remember", command=remember).pack(pady=2)
        tk.Button(win, text="Recall", command=recall).pack(pady=2)
        tk.Button(win, text="Forget", command=forget).pack(pady=2)
        tk.Label(win, textvariable=result_var, wraplength=400).pack(pady=10)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)
        win.mainloop()
