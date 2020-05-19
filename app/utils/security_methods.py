import os
import hashlib
import jwt
import time
from base64 import b64encode, b64decode


class Armored():

    def __init__(self):
        pass

    def __hash_password(self, salt, password):

        key = hashlib.pbkdf2_hmac(
            'sha256',  # The hash digest algorithm for HMAC
            password.encode('utf-8'),  # Convert the password to bytes
            salt,  # Provide the salt
            100000  # It is recommended to use at least 100,000 iterations of SHA-256
        )

        return {'salt': salt, 'key': key}

    def get_hash(self, password):

        salt = os.urandom(64)

        process = self.__hash_password(salt, password)
        
        hashed = b64encode(process['salt'] + process['key']).decode('utf-8')

        return hashed

    def match_password(self, stored_password, password):

        decoded_password = b64decode(stored_password.encode('utf-8'))

        salt = decoded_password[:64]

        stored_password = decoded_password[64:]

        process = self.__hash_password(salt, password)

        if process['key'] == stored_password:
            return True

        return False

    def get_access_token(self):
        
        
        payload = {
            "iss": 'TCW-AUTH-SERVER',
            "exp": time.time() + 1800
        }

        with open(os.path.dirname(__file__) + '/../keys/private.pem') as private:
            private_key = private.read()

        access_token = jwt.encode(payload, private_key, algorithm= 'RS256')

        return access_token.decode()
