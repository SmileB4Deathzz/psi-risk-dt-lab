import time
import json
import pandas as pd
from confluent_kafka import Producer

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'iot-metrics'

# Initialize Kafka producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Load datasets
baseline_df = pd.read_csv('data/baseline_dataset.csv')
drift_df = pd.read_csv('data/drift_dataset.csv')

def send_metrics(df, device_id):
    """Send metrics from a DataFrame to Kafka."""
    for _, row in df.iterrows():
        message = {
            'device_id': device_id,
            'timestamp': row['timestamp'],
            'sensor_value': row['sensor_value']
        }
        producer.produce(KAFKA_TOPIC, key=str(device_id), value=json.dumps(message))
        producer.flush()
        time.sleep(0.1)  # Simulate delay between messages

if __name__ == "__main__":
    print("Starting Kafka producer...")
    send_metrics(baseline_df, device_id=1)
    send_metrics(drift_df, device_id=2)
    print("All metrics sent.")