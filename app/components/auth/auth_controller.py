from .auth_pb2_grpc import DataProcessorServicer, add_DataProcessorServicer_to_server
from ...utils import Database, Armored
from . import auth_pb2 as auth_proto


class AuthController(DataProcessorServicer):

    def __init__(self):
        self.__db = Database()
        self.__armor = Armored()

    def GetData(self, request, context):
        context.set_code(405)
        context.set_details('troll')
        raise NotImplementedError('troll')

    def PostData(self, request, context):
        try:

            data = self.__db.find('users', {"username": request.username})

            valid = self.__armor.match_password(
                data['data'][0]['password'], request.password)
            if valid:
                data_response = {
                    "access_code": self.__armor.get_access_token()}

            response = auth_proto.DataResponse(data=data_response)

            return response
        except Exception as error:
            print(error)
            context.set_code(500)
            context.set_details('Explode')
            raise AssertionError('Explode')

    def add_service_to_server(self, service, server):
        add_DataProcessorServicer_to_server(service, server)
