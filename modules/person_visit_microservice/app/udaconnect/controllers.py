import logging

from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import PersonLocationVisit
from flask import request
from flask_accepts import accepts
from flask_restx import Namespace, Resource

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-api-controller")


@api.route("/person-visit")
class ServiceResource(Resource):
    @accepts(schema=LocationSchema)
    def post(self):
        location = request.get_json()
        logger.debug(location)
        status = PersonLocationVisit.create(location)

        return status
