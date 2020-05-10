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
        self._validation_schema = validation_schema

    def process_message(self):
        try:
            received_data = self._socket.recv_json(flags=zmq.NOBLOCK)
            if self._validation_schema:
                validate(instance=received_data, schema=self._validation_schema)
            processed_data = self._transformer(received_data)
            self._socket.send_json(processed_data)
        except zmq.ZMQError:
            pass
        except ValidationError as ve:
            self._socket.send_json({"success": "no", "message": f"{ve.message}"})
