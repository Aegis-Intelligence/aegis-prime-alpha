# aegis_prime_launcher.py — Aegis Prime Alpha Master Launcher

from logger import AegisLogger
from vault_manager import MemoryVaultManager
from directive_manager import DirectiveHierarchyManager
from voiceprint_manager import VoiceprintManager
from ambient_monitor import AmbientMonitorManager
from learning_console import LearningConsoleManager
from persona_sculptor import PersonaSculptorManager
from tactical_simulator import TacticalSimulatorManager
from mission_analyzer import MissionAnalyzerManager
from loyalty_circuit import LoyaltyCircuitManager
from sandbox_simulator import SandboxThreatSimulatorManager
from self_healing import SelfHealingManager

import tkinter as tk
import traceback

def main():
    logger = AegisLogger()

    # Run Self-Healing at boot
    self_healer = SelfHealingManager(logger)
    self_healer.run_full_integrity_check()

    directives_manager = DirectiveHierarchyManager(logger)
    directives = directives_manager.load_directives()

    loyalty_circuit = LoyaltyCircuitManager(logger, directives_manager)
    try:
        loyalty_circuit.verify_loyalty_integrity()
        if loyalty_circuit.check_protocol_frostlock():
            logger.log("Protocol Frostlock engaged. Halting system.")
            return
    except Exception as e:
        logger.log(f"System halted: {e}")
        return

    # Prompt for voice enrollment or verification
    voice_manager = VoiceprintManager(logger)
    mode = input("Mode: [boot] | [enroll-voice]: ").strip().lower()
    if mode == "enroll-voice":
        voice_manager.record_voice_sample()
        directives_manager.save_directives()
        return
    else:
        if not voice_manager.verify_voiceprint(directives):
            logger.log("Voiceprint verification failed. Access denied.")
            return

    master_password = input("Enter master override password: ").strip()
    vault_manager = MemoryVaultManager(master_password, logger)
    vault_manager.initialize_vault()
    vault_manager.load_vault()

    # Main GUI launcher
    root = tk.Tk()
    root.title("Aegis Prime Alpha")
    root.geometry("400x400")

    # Subsystem managers
    ambient = AmbientMonitorManager(logger, master_password, vault_manager, directives_manager)
    learning = LearningConsoleManager(logger, vault_manager)
    persona = PersonaSculptorManager(logger, directives_manager, vault_manager)
    tactical = TacticalSimulatorManager(logger, vault_manager)
    analyzer = MissionAnalyzerManager(logger, vault_manager, directives_manager)
    sandbox = SandboxThreatSimulatorManager(logger, vault_manager, directives_manager)

    tk.Button(root, text="View Ambient Monitor", command=ambient.launch_dashboard).pack(pady=5)
    tk.Button(root, text="Launch Learning Console", command=learning.launch_learning_console).pack(pady=5)
    tk.Button(root, text="Open Persona Sculptor", command=persona.launch_persona_sculptor).pack(pady=5)
    tk.Button(root, text="Run Tactical Simulator", command=tactical.launch_simulator).pack(pady=5)
    tk.Button(root, text="Run Tactical Analyzer", command=analyzer.analyze_tactics).pack(pady=5)
    tk.Button(root, text="Run Sandbox Simulator", command=sandbox.run_sandbox_simulation).pack(pady=5)
    tk.Button(root, text="Exit", command=root.destroy).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        input("Press Enter to close.")
