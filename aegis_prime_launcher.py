# === Aegis Prime Sovereign Launcher v3 ===
# Fully integrated sovereign deployment with Sovereign Execution Core Shell Module 1 active

import tkinter as tk
import os

# Core managers
from logger import Logger
from vault_manager import VaultManager
from directives_manager import DirectivesManager

# Core tactical modules
from tactical_simulator_manager import TacticalSimulatorManager
from mission_analyzer_manager import MissionAnalyzerManager
from loyalty_circuit_manager import LoyaltyCircuitManager
from sandbox_threat_simulator_manager import SandboxThreatSimulatorManager
from self_healing_manager import SelfHealingManager

# Sovereign cognitive expansion modules
from tactical_analyzer_gui import TacticalAnalyzerGUI
from sandbox_simulator_gui import SandboxSimulatorGUI
from adaptive_learning_engine import AdaptiveLearningEngine
from conversational_interface import ConversationalInterface
from diplomacy_engine_v3 import DiplomacyEngineV3
from external_learning_engine import ExternalLearningEngine
from cognitive_firewall import CognitiveFirewall
from commander_dashboard import CommanderDashboard
from tactical_scenario_generator import TacticalScenarioGenerator
from system_operator_interface import SystemOperatorInterface

# Sovereign Execution Core Module 1
from sovereign_code_validator import SovereignCodeValidator

# === Initialize Core Systems ===

logger = Logger()
vault_manager = VaultManager(logger)
directives_manager = DirectivesManager(logger)

# Initialize Sovereign Code Validator
watch_modules = [
    'logger.py',
    'vault_manager.py',
    'directives_manager.py',
    'loyalty_circuit_manager.py',
    'tactical_simulator_manager.py',
    'mission_analyzer_manager.py',
    'sandbox_threat_simulator_manager.py',
    'self_healing_manager.py',
    'adaptive_learning_engine.py',
    'conversational_interface.py',
    'diplomacy_engine_v3.py',
    'external_learning_engine.py',
    'cognitive_firewall.py',
    'commander_dashboard.py',
    'tactical_scenario_generator.py',
    'system_operator_interface.py'
]

code_validator = SovereignCodeValidator(logger, watch_modules)

# Validate code integrity before full launch
if not code_validator.validate_code_integrity():
    logger.log("Code integrity compromised. Sovereign lockdown engaged. Aborting startup.")
    exit(1)

# === Initialize Sovereign Modules ===

tactical_sim = TacticalSimulatorManager(logger, vault_manager)
mission_analyzer = MissionAnalyzerManager(logger, vault_manager, directives_manager)
loyalty_circuit = LoyaltyCircuitManager(logger, directives_manager)
sandbox_threat_sim = SandboxThreatSimulatorManager(logger, vault_manager, directives_manager)
self_healer = SelfHealingManager(logger)

tactical_analyzer = TacticalAnalyzerGUI(logger, vault_manager, directives_manager)
sandbox_gui = SandboxSimulatorGUI(logger, vault_manager, directives_manager)
adaptive_learning = AdaptiveLearningEngine(logger, vault_manager, directives_manager)
conversation_gui = ConversationalInterface(logger, vault_manager, directives_manager)
diplomacy_engine = DiplomacyEngineV3(logger, vault_manager, directives_manager)
external_learning = ExternalLearningEngine(logger, vault_manager, directives_manager)
cognitive_firewall = CognitiveFirewall(logger, vault_manager, directives_manager)
commander_dashboard = CommanderDashboard(logger, vault_manager, directives_manager, cognitive_firewall)
scenario_generator = TacticalScenarioGenerator(logger)
system_operator = SystemOperatorInterface(logger)

# === Launch Sovereign Control Console ===

root = tk.Tk()
root.title("Aegis Prime Sovereign Control Console")
root.geometry("600x800")

tk.Label(root, text="Aegis Prime Sovereign AI", font=("Arial", 16, "bold")).pack(pady=10)

# Core operations
tk.Button(root, text="View Memory Vault", command=vault_manager.launch_vault_viewer).pack(pady=5)
tk.Button(root, text="Launch Learning Console", command=vault_manager.launch_learning_console).pack(pady=5)
tk.Button(root, text="Run Tactical Simulator", command=tactical_sim.launch_simulator).pack(pady=5)
tk.Button(root, text="Run Tactical Analyzer", command=tactical_analyzer.analyze_tactics).pack(pady=5)
tk.Button(root, text="Run Sandbox Threat Simulator", command=sandbox_gui.launch_gui).pack(pady=5)
tk.Button(root, text="Run Diplomacy Engine v3", command=diplomacy_engine.launch_diplomacy_gui).pack(pady=5)
tk.Button(root, text="External Learning Ingestion", command=external_learning.launch_learning_gui).pack(pady=5)

# Cognitive interfaces
tk.Button(root, text="Open Conversational Interface (Text)", command=conversation_gui.launch_conversation).pack(pady=5)

# System intelligence
tk.Button(root, text="Launch Commander Dashboard", command=commander_dashboard.launch_dashboard).pack(pady=5)
tk.Button(root, text="Generate Tactical Scenario", command=scenario_generator.launch_scenario_gui).pack(pady=5)
tk.Button(root, text="Run Cognitive Firewall Scan", command=cognitive_firewall.full_firewall_scan).pack(pady=5)

# Operator control
tk.Button(root, text="Open System Operator Interface", command=system_operator.launch_operator_gui).pack(pady=5)

# Exit button
tk.Button(root, text="Exit Sovereign Console", command=root.destroy).pack(pady=20)

root.mainloop()


# Exit button
tk.Button(root, text="Exit Sovereign Console", command=root.destroy).pack(pady=20)

root.mainloop()
