from .auth_pb2_grpc import DataProcessorServicer, add_DataProcessorServicer_to_server
from ...utils import Database, Armored, BusService
from . import auth_pb2 as auth_proto
import json


class AuthController(DataProcessorServicer):

    def __init__(self):
        self.__db = Database()
        self.__armor = Armored()
        self.bus = BusService(self.verify_data)
        self.bus.listen('rpc_queue')

    def GetData(self, request, context):
        context.set_code(405)
        context.set_details('troll')
        raise NotImplementedError('troll')

    def PostData(self, request, context):
        try:

            data = self.__db.find('users', {"username": request.username})

            print(data)

            if not data['count']:
                raise Exception('Not users registered')

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
            context.set_details(str(error))
            raise AssertionError(str(error))

    def verify_data(self, ch, method, props, body, pika):

        request = json.loads(body)

        data = self.__armor.verify_access_token(request['access_token'])

        response = {
            'result': data[0],
            'message': data[1]
        }

        ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(
            content_type='application/json', delivery_mode=1, correlation_id=props.correlation_id), body=json.dumps(response))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def add_service_to_server(self, service, server):
        add_DataProcessorServicer_to_server(service, server)
