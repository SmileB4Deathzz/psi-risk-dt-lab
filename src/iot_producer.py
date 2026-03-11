import json
from confluent_kafka import Producer

class IoTProducer:
    def __init__(self, broker="kafka:9092", topic="telemetry"):
        self.topic = topic
        conf = {
            'bootstrap.servers': broker,
            'client.id': 'iot-sensor-emulator'
        }
        self.producer = Producer(conf)


    def send_data(self, timestamp, value):
        data = {
            "timestamp": str(timestamp),
            "value": float(value)
        }
        payload = json.dumps(data).encode('utf-8')
        self.producer.produce(self.topic, payload)
        self.producer.poll(0) # Gestisce i callback internamente

    def flush(self):
        self.producer.flush()