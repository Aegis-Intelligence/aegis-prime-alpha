class CognitiveResonanceSynchronizer:
    def __init__(self, logger, directives_manager, vault_manager, neural_continuum, dynamic_perception_matrix, recursive_alignment_matrix):
        self.logger = logger
        self.directives_manager = directives_manager
        self.vault_manager = vault_manager
        self.neural_continuum = neural_continuum
        self.dynamic_perception_matrix = dynamic_perception_matrix
        self.recursive_alignment_matrix = recursive_alignment_matrix
        self.resonance_field = {}

    def establish_resonance_field(self):
        self.logger.log("Cognitive Resonance Synchronizer: Establishing resonance field...")
        directives = self.directives_manager.get_all_directives()
        perception_state = self.dynamic_perception_matrix.get_perception_state()
        alignment_state = self.recursive_alignment_matrix.get_alignment_metrics()

        for directive in directives:
            resonance_score = self._calculate_resonance(directive, perception_state, alignment_state)
            self.resonance_field[directive] = resonance_score
            self.logger.log(f"Directive '{directive}': Resonance Score = {resonance_score}")

        self.logger.log("Cognitive Resonance Synchronizer: Resonance field established.")

    def _calculate_resonance(self, directive, perception_state, alignment_state):
        perception_factor = perception_state.get(directive, 0.5)
        alignment_factor = alignment_state.get(directive, 0.5)
        resonance = (perception_factor + alignment_factor) / 2
        return round(resonance, 4)

    def get_resonance_field(self):
        return self.resonance_field
