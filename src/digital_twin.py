import json
import numpy as np
from confluent_kafka import Consumer, KafkaError
from entropy_metrics import compute_all_metrics
from drift_detection import calc_delta_h
from risk_signal import generate_risk_score, format_risk_message

class DigitalTwinConsumer:
    def __init__(self, broker="kafka:9092", topic="telemetry", group="dt-analysis"):
        conf = {
            'bootstrap.servers': broker,
            'group.id': group,
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(conf)
        self.consumer.subscribe([topic])
        self.baseline = None

    def consume_window(self, window_size=500, timeout_ms=30000):
        """
        Legge da Kafka finché non accumula una finestra completa di dati.
        Ritorna un array numpy pronto per l'analisi.
        timeout_ms: massimo tempo in millisecondi per attendere i dati
        """
        window_data = []
        print(f"📥 Accumulo finestra di {window_size} campioni (timeout: {timeout_ms}ms)...")
        
        start_time = __import__('time').time() * 1000
        eof_count = 0
        MAX_EOF_RETRIES = 3
        
        while len(window_data) < window_size:
            # Check timeout
            simulated_time = __import__('time').time() * 1000 - start_time
            if simulated_time > timeout_ms:
                print(f"⚠️  Timeout raggiunto dopo {simulated_time:.0f}ms. Raccolti {len(window_data)}/{window_size} campioni.")
                break
            
            msg = self.consumer.poll(1.0)  # Timeout di 1 secondo per poll
            
            if msg is None: 
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    eof_count += 1
                    if eof_count >= MAX_EOF_RETRIES:
                        print(f"⚠️  Fine partizione raggiunta. Raccolti {len(window_data)}/{window_size} campioni.")
                        break
                    continue
                else:
                    print(f"❌ Errore Kafka: {msg.error()}")
                    break
            
            eof_count = 0  # Reset EOF counter on successful message
            payload = json.loads(msg.value().decode('utf-8'))
            window_data.append(payload['value'])
            
        return np.array(window_data)

    def analyse_metrics(self, window_size=500, timeout_ms=30000):
        """
        Consumes a window of data and computes entropy metrics internally.
        Returns a dictionary with metrics computed on the window.
        """
        window = self.consume_window(window_size=window_size, timeout_ms=timeout_ms)
        if len(window) == 0:
            return None
        metrics = compute_all_metrics(window)
        metrics['n_samples'] = len(window)
        if self.baseline is not None:
            delta_h = calc_delta_h(metrics['shannon'], self.baseline['shannon_mean'])
            risk_level = generate_risk_score(delta_h, self.baseline['shannon_std'])
            
            if risk_level >= 1:  # Warning or Critical
                self.mitigate_risk(risk_level)
                print(f"⚠️  Rischio rilevato: {format_risk_message(risk_level)} (ΔH={delta_h:.4f})")
    
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