class HorizonPredictionEngine:
    def __init__(self, logger, cognitive_correlation, predictive_threat, neural_continuum):
        self.logger = logger
        self.cognitive_correlation = cognitive_correlation
        self.predictive_threat = predictive_threat
        self.neural_continuum = neural_continuum

    def forecast_operational_horizon(self):
        self.logger.log("[HorizonPrediction] Initiating operational horizon forecast.")

        correlation_strength = self.cognitive_correlation.evaluate_correlation_strength()
        predicted_threats = self.predictive_threat.generate_forecast_window()
        continuum_stability = self.neural_continuum.evaluate_continuum_coherence()

        horizon_score = self.calculate_horizon_score(correlation_strength, predicted_threats, continuum_stability)

        if horizon_score >= 85:
            self.logger.log("[HorizonPrediction] Forecast: OPTIMAL OPERATIONAL WINDOW.")
        elif 60 <= horizon_score < 85:
            self.logger.log("[HorizonPrediction] Forecast: STABLE but CAUTION ADVISED.")
        elif 40 <= horizon_score < 60:
            self.logger.log("[HorizonPrediction] Forecast: DEGRADED OPERATIONS — Tactical adjustments recommended.")
        else:
            self.logger.log("[HorizonPrediction] Forecast: CRITICAL INSTABILITY — Immediate strategic review required.")

    def calculate_horizon_score(self, correlation_strength, predicted_threats, continuum_stability):
        threat_penalty = len(predicted_threats) * 5
        score = (correlation_strength * 0.5) + (continuum_stability * 0.4) - threat_penalty
        score = max(min(score, 100), 0)
        self.logger.log(f"[HorizonPrediction] Calculated Horizon Score: {score}")
        return score
