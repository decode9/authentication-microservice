from .grpcAPI import Beetle
from .components import RegisterController, AuthController


app = Beetle()

app.services = [
    RegisterController(),
    AuthController()
]
