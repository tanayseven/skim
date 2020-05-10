from time import sleep
from typing import Callable

import zmq
from jsonschema import validate, ValidationError


class ZmqServer:
    def __init__(
        self, transformer: Callable[[dict], dict], port=5555, validation_schema=None
    ):
        self._transformer = transformer
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f"tcp://*:{port}")
        self._socket = socket
        self._listening = False
        self._validation_schema = validation_schema

    def start(self):
        self._listening = True
        while self._listening:
            sleep(0.1)
            try:
                received_data = self._socket.recv_json(flags=zmq.NOBLOCK)
                if self._validation_schema:
                    validate(instance=received_data, schema=self._validation_schema)
                processed_data = self._transformer(received_data)
                self._socket.send_json(processed_data)
            except zmq.ZMQError:
                pass
            except ValidationError as ve:
                self._socket.send_json(
                    {"success": "no", "message": f"{ve.message}",}
                )

    def stop(self):
        self._listening = False
