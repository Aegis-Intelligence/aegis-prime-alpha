# vault_manager.py — Aegis Prime Sovereign Memory Vault Manager

import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import simpledialog, messagebox

VAULT_FILE = "aegis_memory.vault"
VAULT_BACKUP_FILE = "aegis_memory_backup.vault"

class VaultManager:
    def __init__(self, logger):
        self.logger = logger
        self.master_password = None
        self.vault_data = {}

    # Key generation
    def generate_key(self, master_password):
        digest = hashlib.sha256(master_password.encode()).digest()
        return base64.urlsafe_b64encode(digest)

    # Encryption
    def encrypt_data(self, data, key):
        return Fernet(key).encrypt(data.encode())

    def decrypt_data(self, token, key):
        return Fernet(key).decrypt(token).decode()

    # Vault initialization
    def initialize_vault(self, master_password):
        self.master_password = master_password
        key = self.generate_key(master_password)
        if os.path.exists(VAULT_FILE):
            self.logger.log("Vault already exists.")
            return
        encrypted = self.encrypt_data("{}", key)
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypted)
        self.logger.log("Memory Vault initialized and encrypted.")

    # Load vault
    def load_vault(self, master_password):
        self.master_password = master_password
        key = self.generate_key(master_password)
        try:
            with open(VAULT_FILE, "rb") as f:
                encrypted = f.read()
            decrypted = self.decrypt_data(encrypted, key)
            self.vault_data = json.loads(decrypted)
            self.logger.log("Vault loaded successfully.")
        except Exception as e:
            self.logger.log(f"Vault access failed: {e}")
            self.vault_data = {}

    # Save vault
    def save_vault(self):
        key = self.generate_key(self.master_password)
        encrypted = self.encrypt_data(json.dumps(self.vault_data), key)
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypted)
        self.logger.log("Vault updated.")
        # Auto-backup
        with open(VAULT_BACKUP_FILE, "wb") as f:
            f.write(encrypted)
        self.logger.log("Vault backup created.")

    # Vault viewer GUI
    def launch_vault_viewer(self):
        win = tk.Toplevel()
        win.title("Aegis Sovereign Vault Viewer")
        win.geometry("600x500")
        tk.Label(win, text="Decrypted Memory Vault", font=("Arial", 14)).pack(pady=10)
        box = tk.Text(win, height=25, width=70)
        box.pack()
        box.insert(tk.END, json.dumps(self.vault_data, indent=2))
        box.config(state=tk.DISABLED)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)
        self.logger.log("Vault viewer accessed.")

    # Learning Console GUI
    def launch_learning_console(self):
        win = tk.Toplevel()
        win.title("Aegis Learning Console")
        win.geometry("500x450")

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

        def remember_entry():
            k, v = key_var.get(), value_var.get()
            mission = mission_var.get()
            if mission not in self.vault_data:
                self.vault_data[mission] = {}
            self.vault_data[mission][k] = v
            self.save_vault()
            result_var.set("Memory updated.")
            self.logger.log(f"[LEARN] {mission} → {k} = {v}")

        def recall_entry():
            k = key_var.get()
            mission = mission_var.get()
            value = self.vault_data.get(mission, {}).get(k, "[Memory Not Found]")
            result_var.set(value)
            self.logger.log(f"[RECALL] {mission} → {k}: {value}")

        def forget_entry():
            k = key_var.get()
            mission = mission_var.get()
            if mission in self.vault_data and k in self.vault_data[mission]:
                del self.vault_data[mission][k]
                self.save_vault()
                result_var.set("Entry removed.")
                self.logger.log(f"[FORGET] {mission} → {k} deleted")

        tk.Button(win, text="Remember", command=remember_entry).pack(pady=2)
        tk.Button(win, text="Recall", command=recall_entry).pack(pady=2)
        tk.Button(win, text="Forget", command=forget_entry).pack(pady=2)
        tk.Label(win, textvariable=result_var).pack(pady=10)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=5)
