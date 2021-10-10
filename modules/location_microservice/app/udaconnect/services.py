import logging
from datetime import datetime
from typing import Dict, List

from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_Point
from sqlalchemy.sql import text

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("locations-api")


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
                .filter(Location.id == location_id)
                .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        return new_location

    @staticmethod
    def retrieve_locations_for_person(person_id: int, start_date: datetime, end_date: datetime
                                      ) -> List[Location]:
        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        return locations

    @staticmethod
    def retrieve_locations_for_line(line) -> List[Location]:

        line['person_id'] = int(line['person_id'])
        line['meters'] = int(line['meters'])
        logger.debug("Print line...")
        logger.debug(line)

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )

        locations = []
        for (
                exposed_person_id,
                location_id,
                exposed_lat,
                exposed_long,
                exposed_time,
        ) in db.engine.execute(query, **line):
            location = Location(
                id=location_id,
                person_id=exposed_person_id,
                creation_time=exposed_time.isoformat(),
            )
            location.set_wkt_with_coords(exposed_lat, exposed_long)

            result = {
                "person_id": exposed_person_id,
                "id": location_id,
                "latitude": exposed_lat,
                "longitude": exposed_long,
                "creation_time": exposed_time.isoformat()
            }

            locations.append(result)

        return locations
