from confluent_kafka import Consumer

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'iot-metrics'

# Initialize Kafka consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'auto.offset.reset': 'smallest'
})

