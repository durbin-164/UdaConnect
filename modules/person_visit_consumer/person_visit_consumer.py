from json import loads

import requests
from kafka import KafkaConsumer

LOCATION_SERVICE_ENDPOINT = 'http://localhost:30016/'

KAFKA_SERVER = 'localhost:9092'
KAFKA_TOPICS = 'person_location_visits'

consumer = KafkaConsumer(
    KAFKA_TOPICS,
    bootstrap_servers=[KAFKA_SERVER],
    value_deserializer=lambda x: loads(x.decode('utf-8')))

print("Consumer start...")
for message in consumer:
    location = message.value
    print(location)

    new_location = requests.post(LOCATION_SERVICE_ENDPOINT + "api/locations", json=location)


