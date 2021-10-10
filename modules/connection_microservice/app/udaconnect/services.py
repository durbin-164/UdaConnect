import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List

import grpc

import requests
from app.udaconnect.models import Connection, Location, Person

from app.config import PERSON_SERVICE_ENDPOINT_GRPC, LOCATION_SERVICE_ENDPOINT

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-api")
DATE_FORMAT = "%Y-%m-%d"

from app.udaconnect import person_pb2
from app.udaconnect import person_pb2_grpc

logger.debug("GRPC>>>")
logger.debug(PERSON_SERVICE_ENDPOINT_GRPC)
logger.debug(LOCATION_SERVICE_ENDPOINT)

channel = grpc.insecure_channel(PERSON_SERVICE_ENDPOINT_GRPC)
person_stub = person_pb2_grpc.PersonServiceStub(channel)


class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: str, end_date: str, meters=5
                      ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        locations: List = LocationService.retrieve_locations_for_person(person_id,
                                                                        start_date,
                                                                        end_date)

        # Cache all users in memory for quick lookup
        person_map: Dict[str, Person] = {person.id: person for person in PersonServicegRPC.retrieve_all()}

        # Prepare arguments for queries
        start_date: datetime = datetime.strptime(start_date, DATE_FORMAT)
        end_date: datetime = datetime.strptime(end_date, DATE_FORMAT)

        data = []
        for location in locations:
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )

        result: List[Connection] = []
        for line in tuple(data):
            logger.debug("Print line...")
            logger.debug(line)
            locations_dict = LocationService.retrieve_locations_for_line(line)
            for location_dict in locations_dict:
                location = Location(**location_dict)
                result.append(
                    Connection(
                        person=person_map[location.person_id], location=location,
                    )
                )
        logger.debug("The End....")
        return result


class LocationService:
    @staticmethod
    def retrieve_locations_for_person(person_id: int, start_date: str, end_date: str) -> List[Location]:
        locations = requests.get(
            LOCATION_SERVICE_ENDPOINT + f"api/persons/{person_id}/locations?start_date={start_date}&end_date={end_date}")

        logger.debug("get locations....")
        logger.debug(locations)
        locations = locations.json()

        logger.debug(locations)

        new_locations = []
        for location in locations:
            new_locations.append(Location(**location))
        return new_locations

    @staticmethod
    def retrieve_locations_for_line(line):
        locations = requests.get(
            LOCATION_SERVICE_ENDPOINT + f"api/location/locations?line={json.dumps(line)}")
        logger.debug("all locations...")
        logger.debug(locations)
        return locations.json()


class PersonServicegRPC:
    @staticmethod
    def retrieve_all() -> List[Person]:
        response = person_stub.RetrieveAll(person_pb2.Empty())
        persons = response.persons
        logger.debug("Persons....")
        logger.debug(persons)
        return persons
