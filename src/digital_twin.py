import json
import numpy as np
from confluent_kafka import Consumer, KafkaError
from entropy_metrics import compute_all_metrics
from drift_detection import calc_delta_h
from risk_signal import generate_risk_score, format_risk_message

class DigitalTwinConsumer:
    def __init__(self, broker="kafka:9092", topic="telemetry", group="dt-analysis", window_size=500, step=100):
        conf = {
            'bootstrap.servers': broker,
            'group.id': group,
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(conf)
        self.consumer.subscribe([topic])
        self.window_size = window_size
        self.step = step
        self.buffer = []
        self.baseline = None

    def consume_window(self, timeout_ms=30000):
        import time
        start_time = time.time() * 1000

        while len(self.buffer) < self.window_size + self.step:
            if (time.time() * 1000 - start_time) > timeout_ms:
                break
            msg = self.consumer.poll(1.0)
            if msg and not msg.error():
                payload = json.loads(msg.value().decode('utf-8'))
                self.buffer.append(payload['value'])
            
        self.buffer = self.buffer[-self.window_size:]
        print(f"Consumed {len(self.buffer)} samples for analysis.")
        return np.array(self.buffer)

    def analyse_metrics(self, timeout_ms=30000):
        """
        Consumes a sliding window of data and computes entropy metrics internally.
        Returns a dictionary with metrics computed on the window.
        """
        window = self.consume_window(timeout_ms=timeout_ms)
        if len(window) == 0:
            return None
        metrics = compute_all_metrics(window)
        metrics['n_samples'] = len(window)
        if self.baseline is not None:
            delta_h = calc_delta_h(metrics['shannon'], self.baseline['shannon_mean'])
            risk_level = generate_risk_score(delta_h, self.baseline['shannon_std'])
            if risk_level >= 1:  # Warning or Critical
                self.mitigate_risk(risk_level)
                print(f"Risk detected! ΔH: {delta_h:.4f}, Risk Level: {risk_level}, Message: {format_risk_message(risk_level)}")
            metrics['delta_h'] = delta_h
            metrics['risk_level'] = risk_level
            metrics['risk_message'] = format_risk_message(risk_level)
        return metrics
    
    def mitigate_risk(self, risk_level):
        # Placeholder for risk mitigation logic
        pass

    def set_baseline(self, baseline):
        self.baseline = baseline

    def close(self):
        self.consumer.close()