from typing import Optional, List

from app.udaconnect.schemas import (
    ConnectionSchema,
    PersonSchema
)
from app.udaconnect.services import ConnectionService, PersonServicegRPC
from app.udaconnect.models import Person
from flask import request
from flask_accepts import responds
from flask_restx import Namespace, Resource

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        distance: Optional[int] = request.args.get("distance", 5)
        start_date = request.args["start_date"]
        end_date = request.args["end_date"]

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results


@api.route("/persons")
class PersonResource(Resource):
    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonServicegRPC.retrieve_all()
        return persons
