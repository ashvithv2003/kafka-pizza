import random
import time
from faker import Faker
from faker.providers import BaseProvider
from confluent_kafka import Producer
import json

class PizzaProvider(BaseProvider):
    def pizza_name(self):
        valid_pizza_names = [
            'Margherita',
            'Marinara',
            'Diavola',
            'Mari & Monti',
            'Salami',
            'Pepperoni'
        ]
        return valid_pizza_names[random.randint(0, len(valid_pizza_names) - 1)]

# Set up Faker with the PizzaProvider
fake = Faker()
fake.add_provider(PizzaProvider)

# Kafka configuration
TOPIC_NAME = "demo"
conf = {
    'bootstrap.servers': "kafka-demo-ashvithv2003-06ec.f.aivencloud.com:28574",
    'security.protocol': 'SSL',
    'ssl.ca.location': 'ca.pem',
    'ssl.certificate.location': 'service.cert',
    'ssl.key.location': 'service.key'
}

producer = Producer(**conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

try:
    for i in range(100):
        pizza_name = fake.pizza_name()
        customer_details = {
            'name': fake.name(),
            'address': fake.address(),
            'phone': fake.phone_number()
        }
        message = {
            'order_number': i + 1,
            'pizza_name': pizza_name,
            'customer_details': customer_details
        }
        message_json = json.dumps(message)
        producer.produce(TOPIC_NAME, key=str(i), value=message_json.encode('utf-8'), callback=delivery_report)
        producer.poll(0)
        print(f"Message sent: {message_json}")
        time.sleep(1)
finally:
    producer.flush()
    print("Producer closed")
