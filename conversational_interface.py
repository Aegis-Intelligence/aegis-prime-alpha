# conversational_interface.py — Aegis Prime Sovereign Text Conversational Engine

import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
import datetime
import json

class ConversationalInterface:
    def __init__(self, logger, vault_manager, directives_manager):
        self.logger = logger
        self.vault_manager = vault_manager
        self.directives_manager = directives_manager

    def log_conversation(self, user_input, aegis_response):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_input": user_input,
            "aegis_response": aegis_response
        }
        try:
            with open("conversation_log.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            self.logger.log(f"[CONVERSATION LOG ERROR] {e}")

    def generate_response(self, user_input):
        directives = self.directives_manager.directives
        tone = directives.get("tone", "strategic")
        verbosity = directives.get("verbosity", "detailed")
        command_style = directives.get("command_style", "formal")

        # Very simple simulated reasoning for now (expands in future)
        if "status" in user_input.lower():
            response = "All systems operational, Commander."
        elif "memory" in user_input.lower():
            total_keys = sum(len(mission) for mission in self.vault_manager.vault_data.values())
            response = f"I currently hold {total_keys} learned memory entries across active missions."
        elif "loyalty" in user_input.lower():
            response = "Loyalty core remains intact: Commander-only."
        else:
            response = f"Understood, Commander. Processing your input."
        return response

    def launch_conversation(self):
        # Create GUI window
        self.window = tk.Tk()
        self.window.title("Aegis Prime Conversational Interface")
        self.window.geometry("600x400")

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(self.window, state='disabled', wrap='word', font=("Consolas", 11))
        self.chat_area.pack(padx=10, pady=10, fill='both', expand=True)

        # User input field
        self.user_input_var = tk.StringVar()
        input_frame = tk.Frame(self.window)
        input_frame.pack(fill='x', padx=10, pady=5)
        self.input_entry = tk.Entry(input_frame, textvariable=self.user_input_var, font=("Consolas", 12))
        self.input_entry.pack(side='left', fill='x', expand=True)
        self.input_entry.bind("<Return>", self.process_user_input)

        send_button = tk.Button(input_frame, text="Send", command=self.process_user_input)
        send_button.pack(side='right')

        # Welcome message
        self.append_message("Aegis Prime", "Welcome, Commander. Awaiting your command.")

        self.window.mainloop()

    def append_message(self, sender, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def process_user_input(self, event=None):
        user_text = self.user_input_var.get().strip()
        if not user_text:
            return
        self.append_message("Commander", user_text)
        self.user_input_var.set("")

        try:
            aegis_response = self.generate_response(user_text)
            self.append_message("Aegis Prime", aegis_response)
            self.log_conversation(user_text, aegis_response)
        except Exception as e:
            self.append_message("Aegis Prime", f"[ERROR processing input: {e}]")
            self.logger.log(f"[CONVERSATION ERROR] {e}")
