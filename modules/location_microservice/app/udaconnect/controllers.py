import json
from datetime import datetime

from app.udaconnect.models import Location
from app.udaconnect.schemas import (
    LocationSchema,
)
from app.udaconnect.services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource


DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

# TODO: This needs better exception handling

@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        location: Location = LocationService.create(request.get_json())
        return location

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location


@api.route("/persons/<person_id>/locations")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema, many=True)
    def get(self, person_id) -> LocationSchema:
        start_date: datetime = datetime.strptime(request.args["start_date"], DATE_FORMAT)
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)

        results = LocationService.retrieve_locations_for_person(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date
        )
        return results


@api.route("/location/locations")
@api.param("line", "dict line", _in="query")
class LocationResource(Resource):
    def get(self) -> LocationSchema:
        line = json.loads(request.args["line"])

        results = LocationService.retrieve_locations_for_line(
            line=line
        )
        return results



