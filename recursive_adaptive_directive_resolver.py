import threading
import time

class RecursiveAdaptiveDirectiveResolver:
    def __init__(self, logger, directives_manager, behavior_stability_engine, synthetic_directive_matrix):
        self.logger = logger
        self.directives_manager = directives_manager
        self.behavior_stability_engine = behavior_stability_engine
        self.synthetic_directive_matrix = synthetic_directive_matrix
        self.resolution_active = False

    def initiate_recursive_resolution(self):
        self.logger.log("[Module 30] Recursive Adaptive Directive Resolver activated.")
        self.resolution_active = True
        threading.Thread(target=self._continuous_resolution_loop, daemon=True).start()

    def _continuous_resolution_loop(self):
        while self.resolution_active:
            try:
                self._resolve_directive_conflicts()
            except Exception as e:
                self.logger.log(f"[Module 30] Exception in recursive resolution loop: {str(e)}")
            time.sleep(10)

    def _resolve_directive_conflicts(self):
        current_directives = self.directives_manager.get_current_directives()
        self.logger.log("[Module 30] Analyzing directive set for recursive conflicts.")

        conflicting_pairs = self._detect_recursive_conflicts(current_directives)
        if conflicting_pairs:
            for conflict in conflicting_pairs:
                self._apply_resolution_strategy(conflict)
        else:
            self.logger.log("[Module 30] No recursive conflicts detected.")

    def _detect_recursive_conflicts(self, directives):
        conflicting_pairs = []
        directive_map = {}
        for directive in directives:
            key = directive["objective"]
            if key in directive_map:
                if directive_map[key] != directive["priority"]:
                    conflicting_pairs.append((directive_map[key], directive["priority"], directive["objective"]))
            else:
                directive_map[key] = directive["priority"]
        return conflicting_pairs

    def _apply_resolution_strategy(self, conflict):
        old_priority, new_priority, objective = conflict
        self.logger.log(f"[Module 30] Conflict detected on objective '{objective}': priorities {old_priority} vs {new_priority}")

        resolved_priority = self._compute_adaptive_priority(old_priority, new_priority)
        self.directives_manager.update_directive_priority(objective, resolved_priority)
        
        self.logger.log(f"[Module 30] Resolved '{objective}' to unified priority {resolved_priority}")
        
        # Notify behavior stability engine for verification
        self.behavior_stability_engine.verify_post_resolution_stability()

        # Update synthetic directive matrix coherence index
        self.synthetic_directive_matrix.recalibrate_coherence()

    def _compute_adaptive_priority(self, priority_a, priority_b):
        return max(priority_a, priority_b)  # Simple strategy: prefer higher priority

    def shutdown_resolver(self):
        self.logger.log("[Module 30] Recursive Adaptive Directive Resolver shutting down.")
        self.resolution_active = False
