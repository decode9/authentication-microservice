from .user_pb2_grpc import DataProcessorServicer
from ...utils import Database
from . import user_pb2 as user_proto


class UserController(DataProcessorServicer):

    def __init__(self):
        self.db = Database()

    def GetData(self, request, context):
        try:
            users = self.db.find('users')

            data = []

            if users['count']:

                data = users['data']
            print('Get Response')
            response = user_proto.DataMultipleResponse(
                data=list(data)
            )
            print('Return Response')

            return response
        except Exception as error:
            print(error)
            response = user_proto.DataMultipleResponse(
                data=[]
            )

            return response

    def SaveData(self, request, context):

        try:
            data = {
                "name": request.name,
                "lastname": request.lastname,
                "identification": request.identification,
                "type_identification": request.type_identification,
                "phone_number": request.phone_number
            }

            data = self.db.insert_one('users', data)

            response = user_proto.DataResponse(data=data)

            return response
        except Exception as error:
            print(error)

    def UpdateData(self, request, context):

        try:
            data = {
                "name": request.name,
                "lastname": request.lastname,
                "identification": request.identification,
                "type_identification": request.type_identification,
                "phone_number": request.phone_number
            }

            print('UPDATE')
            print(request._id)


            data = self.db.update_one('users', {"_id": request._id}, data)

            response = user_proto.DataResponse(data=data)

            return response
        except Exception as error:
            print(error)

    def DeleteData(self, request, context):

        try:
            data = {
                "_id": request._id,
            }

            data = self.db.delete_one('users', data)

            response = user_proto.DataResponse(data=data)

            return response
        except Exception as error:
            print(error)
