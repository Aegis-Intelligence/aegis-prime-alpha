# File: dynamic_perception_matrix.py

class DynamicPerceptionMatrix:
    def __init__(self, logger, directives_manager, vault_manager, cognitive_correlation, horizon_predictor, synthetic_directive_matrix):
        self.logger = logger
        self.directives_manager = directives_manager
        self.vault_manager = vault_manager
        self.cognitive_correlation = cognitive_correlation
        self.horizon_predictor = horizon_predictor
        self.synthetic_directive_matrix = synthetic_directive_matrix
        self.perception_map = {}

    def activate_perception_mapping(self):
        self.logger.log("[DynamicPerceptionMatrix] Activating dynamic perception matrix construction...")
        directive_states = self.synthetic_directive_matrix.retrieve_directive_states()
        horizon_vectors = self.horizon_predictor.generate_future_projections()

        for directive in directive_states:
            perception_vector = self._generate_perception_vector(directive, horizon_vectors)
            self.perception_map[directive['id']] = perception_vector
            self.logger.log(f"[DynamicPerceptionMatrix] Directive {directive['id']} mapped into perception space.")

        self.logger.log("[DynamicPerceptionMatrix] Perception matrix initialization complete.")

    def extract_current_mapping(self):
        return self.perception_map

    def _generate_perception_vector(self, directive, horizon_vectors):
        correlation = self.cognitive_correlation.compute_directive_correlation(directive)
        future_projection = horizon_vectors.get(directive['id'], 0.5)
        perception_vector = (correlation + future_projection) / 2.0
        return perception_vector
