# persona_sculptor.py — PersonaSculptorManager Module

import tkinter as tk
from tkinter import messagebox, simpledialog

class PersonaSculptorManager:
    def __init__(self, logger, directives_manager, vault_manager):
        self.logger = logger
        self.directives_manager = directives_manager
        self.vault_manager = vault_manager

    def launch_persona_sculptor(self):
        directives = self.directives_manager.directives

        win = tk.Tk()
        win.title("Aegis Persona Sculptor")
        win.geometry("400x300")

        tone_var = tk.StringVar(value=directives.get("tone", "strategic"))
        verbosity_var = tk.StringVar(value=directives.get("verbosity", "detailed"))
        command_style_var = tk.StringVar(value=directives.get("command_style", "formal"))

        tk.Label(win, text="Tone").pack()
        tk.OptionMenu(win, tone_var, "strategic", "warm", "cold", "neutral").pack()
        tk.Label(win, text="Response Verbosity").pack()
        tk.OptionMenu(win, verbosity_var, "minimal", "detailed", "expressive").pack()
        tk.Label(win, text="Command Style").pack()
        tk.OptionMenu(win, command_style_var, "formal", "informal", "tactical").pack()

        def save_persona():
            directives["tone"] = tone_var.get()
            directives["verbosity"] = verbosity_var.get()
            directives["command_style"] = command_style_var.get()
            self.directives_manager.save_directives()
            self.logger.log("Persona traits updated.")
            messagebox.showinfo("Saved", "Persona traits updated.")

        tk.Button(win, text="Save Persona", command=save_persona).pack(pady=10)
        tk.Button(win, text="Close", command=win.destroy).pack()
        win.mainloop()
