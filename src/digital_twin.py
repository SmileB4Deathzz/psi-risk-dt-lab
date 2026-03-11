from confluent_kafka import Consumer


class DigitalTwin:
    def __init__(self):
        self.state = {}

    def update_state(self, data):
        # Update the digital twin's state based on the incoming message
        print(f"Updating digital twin state with data: {data}")
        # Here you would parse the data and update the state accordingly

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'iot-metrics'

# Initialize Kafka consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'auto.offset.reset': 'smallest'
})

running = True
def consume_messages():
    try:
        consumer.subscribe([KAFKA_TOPIC])

        while running:
            msg = consumer.poll(1.0)
            
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            
            # Process the message
            print(f"Received message: {msg.value().decode('utf-8')}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

