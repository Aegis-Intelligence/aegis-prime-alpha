# vault_manager.py — MemoryVaultManager Module

import os
import json
from encryption import VaultEncryption
from constants import VAULT_FILE

class MemoryVaultManager:
    def __init__(self, master_password, logger):
        self.logger = logger
        self.master_password = master_password
        self.encryption = VaultEncryption(master_password)
        self.vault_data = {}

    def initialize_vault(self):
        if os.path.exists(VAULT_FILE):
            self.logger.log("Vault already exists.")
            return
        encrypted = self.encryption.encrypt({})
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypted)
        self.logger.log("Memory Vault initialized and encrypted.")

    def load_vault(self):
        try:
            with open(VAULT_FILE, "rb") as f:
                encrypted = f.read()
            self.vault_data = self.encryption.decrypt(encrypted)
            self.logger.log("Vault loaded successfully.")
            return self.vault_data
        except Exception as e:
            self.logger.log(f"Vault access failed: {e}")
            user_input = input("Vault corrupted. Reset and reinitialize? (y/n): ").lower()
            if user_input == "y":
                os.remove(VAULT_FILE)
                self.initialize_vault()
                self.vault_data = {}
            else:
                self.logger.log("Vault recovery declined by user.")
            return self.vault_data

    def save_vault(self):
        encrypted = self.encryption.encrypt(self.vault_data)
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypted)
        self.logger.log("Vault updated.")
