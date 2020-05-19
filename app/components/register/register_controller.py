from .register_pb2_grpc import DataProcessorServicer, add_DataProcessorServicer_to_server
from ...utils import Database, Armored
from . import register_pb2 as register_proto


class RegisterController(DataProcessorServicer):

    def __init__(self):
        self.__db = Database()
        self.__armor = Armored()

    def GetData(self, request, context):
        context.set_code(400)
        context.set_details('troll')
        raise NotImplementedError('troll')

    def PostData(self, request, context):
        try:
            data = {
                "username": request.username,
                "password": self.__armor.get_hash(request.password),
            }

            data = self.__db.insert_one('users', data)

            response = register_proto.DataResponse(data=data)

            return response
        except Exception as error:
            print(error)
            context.set_code(500)
            context.set_details('Explode')
            raise AssertionError('Explode')

    def add_service_to_server(self, service, server):
        add_DataProcessorServicer_to_server(service, server)
