import logging
from json import loads

import sqlalchemy as db
from kafka import KafkaConsumer
from geoalchemy2.functions import ST_Point

from config import TestingConfig

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("person-visit-consumer-api")

engine = db.create_engine(TestingConfig.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()
metadata = db.MetaData()

TABLE_NAME = 'location'

location_table_db = db.Table(TABLE_NAME, metadata, autoload=True, autoload_with=engine)


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
    query = db.insert(location_table_db).values(id=location['id'],
                                                person_id=location['person_id'],
                                                coordinate=ST_Point(location["latitude"], location["longitude"]),
                                                creation_time=location['creation_time']
                                                )

    result_proxy = connection.execute(query)
    print(result_proxy)
