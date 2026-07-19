# core/integrity_engine.py
from collections import deque
import config

class IntegrityEngine:
    def __init__(self):
        # Rolling double-ended queue to store historical frame status
        self.anomaly_buffer = deque(maxlen=config.TIME_WINDOW_FRAMES)

    def update_and_check(self, frame_has_anomaly):
        self.anomaly_buffer.append(1 if frame_has_anomaly else 0)
        
        if len(self.anomaly_buffer) < config.TIME_WINDOW_FRAMES:
            return False, 100.0  # Warm up phase

        anomaly_ratio = sum(self.anomaly_buffer) / config.TIME_WINDOW_FRAMES
        integrity_score = max(0.0, 100.0 - (anomaly_ratio * 100.0))
        
        # Trigger true alarm if threat patterns persist above your window target
        trigger_alarm = anomaly_ratio >= config.VIOLATION_TRIGGER_PERCENT
        return trigger_alarm, round(integrity_score, 2)