import json
import logging
from concurrent import futures
from datetime import datetime

import grpc
from kafka import KafkaProducer

import location_pb2_grpc
import location_pb2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("person-visit-grpc-api")

KAFKA_SERVER = 'localhost:9092'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda x:
                         json.dumps(x).encode('utf-8'))

topic = "person_location_visits"


class PersonLocationVisitServicer(location_pb2_grpc.PersonLocationVisitServiceServicer):
    def Create(self, request, context):
        location = {
            "id": request.id,
            "person_id": request.person_id,
            "creation_time": datetime.now().isoformat(),
            "longitude": request.longitude,
            "latitude": request.latitude
        }

        producer.send(topic, location)

        producer.flush()

        return location_pb2.LocationMessage(**location)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_PersonLocationVisitServiceServicer_to_server(PersonLocationVisitServicer(), server)

print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
server.wait_for_termination()
