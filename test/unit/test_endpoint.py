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

import pytest
import zmq

from test.unit.fake_zmq import FakeSocket, FakeContext
from skim.endpoint import ZmqServer


def echo(input_json: dict) -> dict:
    return input_json


ECHO_SCHEMA = {
    "type": "object",
    "properties": {"message": {"type": "string"},},
    "required": ["message"],
}


@pytest.fixture
def zmq_client(monkeypatch):
    socket = FakeSocket()
    yield socket


@pytest.fixture
def zmq_server(monkeypatch):
    monkeypatch.setattr(zmq, "Context", FakeContext)
    return ZmqServer(transformer=echo, validation_schema=ECHO_SCHEMA)


def test_connection_echo_success(zmq_client, zmq_server):
    # when
    message = {"message": "Something"}
    zmq_client.send_json(message)
    zmq_server.process_message()

    # then
    received_message = zmq_client.recv_json()
    assert received_message == message


def test_connection_echo_failure(zmq_client, zmq_server):
    # when
    message = {"text": "Something"}
    zmq_client.send_json(message)
    zmq_server.process_message()

    # then
    received_message = zmq_client.recv_json()
    assert received_message["success"] == "no"
    assert "message" in received_message
