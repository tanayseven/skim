# SKIM | Smarter Keyboard Input Method | A simple and smart sentence prediction
# Copyright (C) 2020 Tanay PrabhuDesai

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
        except ValidationError as ve:
            self._socket.send_json({"success": "no", "message": f"{ve.message}"})
