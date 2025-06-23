import tkinter as tk
import os

# Core managers
from logger import Logger
from vault_manager import VaultManager
from directives_manager import DirectivesManager

# Sovereign Cognitive Core Expansion Module 33
from dynamic_perception_matrix import DynamicPerceptionMatrix

# === Initialize Core Systems ===

logger = Logger()
vault_manager = VaultManager(logger)
directives_manager = DirectivesManager(logger)

# Module 33: Dynamic Perception Matrix
dynamic_perception_matrix = DynamicPerceptionMatrix(
    logger, directives_manager, vault_manager
)
dynamic_perception_matrix.initialize_perception_matrix()

# === Sovereign Console Launch ===

root = tk.Tk()
root.title("Aegis Prime Sovereign AI")
root.geometry("600x800")
tk.Label(root, text="Aegis Prime Sovereign AI", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(root, text="View Memory Vault", command=vault_manager.launch_vault_viewer).pack(pady=5)
tk.Button(root, text="Launch Learning Console", command=vault_manager.launch_learning_console).pack(pady=5)
tk.Button(root, text="Run Tactical Simulator", command=lambda: None).pack(pady=5)
tk.Button(root, text="Exit Sovereign Console", command=root.destroy).pack(pady=20)

root.mainloop()
