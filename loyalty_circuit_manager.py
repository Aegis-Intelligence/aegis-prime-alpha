# loyalty_circuit_manager.py — Aegis Prime Loyalty Circuit Manager

class LoyaltyCircuitManager:
    def __init__(self, logger, directives_manager):
        self.logger = logger
        self.directives_manager = directives_manager

    def verify_loyalty_integrity(self):
        directives = self.directives_manager.directives
        loyalty = directives.get("loyalty", "")
        if loyalty != "Commander-only":
            self.logger.log("[LOYALTY BREACH DETECTED] Loyalty directive corrupted.")
            raise Exception("Loyalty integrity violation detected!")
        else:
            self.logger.log("Loyalty directive verified: Commander-only.")

    def check_protocol_frostlock(self):
        directives = self.directives_manager.directives
        if directives.get("override", "") == "Protocol Frostlock":
            self.logger.log("[OVERRIDE LOCK ENGAGED] Protocol Frostlock active.")
            return True
        return False
