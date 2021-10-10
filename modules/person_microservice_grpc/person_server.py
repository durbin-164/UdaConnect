import logging
from concurrent import futures

import grpc

import person_pb2_grpc
import person_pb2
from config import TestingConfig

import sqlalchemy as db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("person-grpc-api")

logger.debug("In person grpc service....")

engine = db.create_engine(TestingConfig.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()
metadata = db.MetaData()

TABLE_NAME = 'person'

person_table_db = db.Table(TABLE_NAME, metadata, autoload=True, autoload_with=engine)


class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def Create(self, request, context):
        pass

    def Get(self, request, context):
        pass

    def RetrieveAll(self, request, context):
        logger.debug("Retrieve all..")
        # Equivalent to 'SELECT * FROM census'
        query = db.select([person_table_db])
        result_proxy = connection.execute(query)
        db_results = result_proxy.fetchall()

        logger.debug("Db operation done...")
        logger.debug(db_results)

        results = person_pb2.PersonMessageList()

        for db_result in db_results:
            person = person_pb2.PersonMessage(
                id=db_result[0],
                first_name=db_result[1],
                last_name=db_result[2],
                company_name=db_result[3]
            )
            results.persons.append(person)

        return results


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)

print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
server.wait_for_termination()
