from concurrent import futures
import grpc
import time
import sys
import os
from pynput import keyboard
import config as conf
from .utils import hotKeys


class Beetle():
    
    services = set()

    def __init__(self, **extraValues):
        self.extraValues = extraValues
        ip = hasattr(conf, 'ip') and conf.ip or '[::]'
        port = hasattr(conf, 'port') and conf.port or '5300'
        self.ip = ip + ':' + port
        self._server = set()

    def __setPrivateKeys(self):
        with open('keys/private.key', 'rb') as f:
            print('Open Private Key')
            private_key = f.read()

        with open('keys/cert.pem', 'rb') as f:
            print('Open Public Key')
            public_key = f.read()

        server_credentials = grpc.ssl_server_credentials(
            ((private_key, public_key))
        )

        return server_credentials

    def __startServer(self):

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        server.add_insecure_port(self.ip)
        print("The server was unsecure")

        if 'secure' in self.extraValues:
            if self.extraValues['secure']:
                credentials = self.__setPrivateKeys()
                server.add_secure_port(self.ip, credentials)
                print("The server was secure")

        print("Server Started in IP " + self.ip)
        self._server = server
        self.__insertControllers()
        server.start()

        self.__loopServer()

    def __loopServer(self, ):
        try:
            print('Press Ctrl+C if you want shutdown the server')
            print('Press Ctrl+U if you want restart the server')
            COMBINATIONS = [
                keyboard.KeyCode(char='\x15'),
                keyboard.KeyCode(char='\x03')
            ]
            hotkey = hotKeys(COMBINATIONS, self.__updateServer)
        except KeyboardInterrupt:
            self._closeServer()

    def __updateServer(self, key):
        try:
            if key == keyboard.KeyCode(char='\x03'):
                self._closeServer()
                print("Server was Stopped")
                exit()

            if key == keyboard.KeyCode(char='\x15'):
                print('Server was Restarted')
                self._closeServer()
                exit()

        except KeyboardInterrupt:
            self._closeServer()

    def __insertControllers(self):

        if len(self.services) != 0:
            for controller in self.services:
                controller.add_service_to_server(
                    controller, self._server
                )

    def _closeServer(self):
        self._server.stop(0)

    def run(self):
        self.__startServer()
