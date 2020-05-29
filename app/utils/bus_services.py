import pika
import json
import uuid
import threading
import config as conf


class BusService():

    def __init__(self, callback_function):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=hasattr(conf, 'service_host') and conf.service_host or '127.0.0.1'))
        self.channel = self.connection.channel()
        self.callback_function = callback_function
        self.listen_channel = 'rpc_queue'

    def TransmitChannel(self):
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

    def on_response(self, ch, method, props, body):
        print('RESPONSE')
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body.decode('utf8'))

    def call(self, channel, my_params):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key=channel,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                content_type='application/json'
            ),
            body=json.dumps(my_params)
        )

        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def on_request(self, ch, method, props, body):
        print('REQUESTED')

        if self.callback_function:
            self.callback_function(ch, method, props, body, pika)
            return

        response = {
            'message': 'Not Implemented'
        }

        ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(
            content_type='application/json', delivery_mode=1, correlation_id=props.correlation_id), body=json.dumps(response))

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __listen_channel(self):
        self.channel.queue_declare(queue=self.listen_channel)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.listen_channel, on_message_callback=self.on_request)
        self.channel.start_consuming()

    def listen(self, channel):
        self.listen_channel = channel
        consumer_thread = threading.Thread(target=self.__listen_channel)
        consumer_thread.start()
