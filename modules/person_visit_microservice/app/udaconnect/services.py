import json
import logging
from datetime import datetime
from typing import Dict

from kafka import KafkaProducer
from app.config import KAFKA_SERVER

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-api")

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda x:
                         json.dumps(x).encode('utf-8'))

topic = "person_location_visits"


class PersonLocationVisit:
    @staticmethod
    def create(location: Dict):
        logger.debug(location)
        location['creation_time'] = datetime.now().isoformat()
        producer.send(topic, location)

        producer.flush()
        return {"status": "ok"}
