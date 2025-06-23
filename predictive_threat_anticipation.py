import time
import json
from collections import deque, Counter

class PredictiveThreatAnticipation:
    def __init__(self, logger):
        self.logger = logger
        self.recent_events = deque(maxlen=1000)
        self.pattern_counter = Counter()
        self.warning_threshold = 5
        self.forecast_logs = []

    # === Feed Events ===

    def register_event(self, event_type, details):
        timestamp = time.time()
        event = {"timestamp": timestamp, "type": event_type, "details": details}
        self.recent_events.append(event)
        self.pattern_counter[event_type] += 1
        self.logger.log(f"Event registered for predictive analysis: {event_type} -> {details}")
        self.analyze_patterns()

    # === Pattern Analysis ===

    def analyze_patterns(self):
        common_patterns = self.pattern_counter.most_common(3)
        self.logger.log(f"Current top recurring patterns: {common_patterns}")

        for event_type, count in common_patterns:
            if count >= self.warning_threshold:
                forecast = f"Potential emerging threat pattern detected: [{event_type}] frequency rising."
                self.logger.log(forecast)
                self.log_forecast(event_type, count, forecast)

    # === Forecast Logging ===

    def log_forecast(self, event_type, count, forecast_message):
        forecast_entry = {
            "timestamp": time.time(),
            "event_type": event_type,
            "frequency": count,
            "forecast": forecast_message
        }
        self.forecast_logs.append(forecast_entry)

    def export_forecast_logs(self, filename="threat_forecast_logs.json"):
        with open(filename, 'w') as f:
            json.dump(self.forecast_logs, f, indent=4)
        self.logger.log(f"Threat forecast logs exported to {filename}.")

    # === Dynamic Threshold Adjustment (Optional) ===

    def set_warning_threshold(self, new_threshold):
        self.warning_threshold = new_threshold
        self.logger.log(f"Updated predictive warning threshold to: {new_threshold}")
