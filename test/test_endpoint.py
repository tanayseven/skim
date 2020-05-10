import pytest
import zmq

from test.fake_zmq import FakeSocket, FakeContext
from skim.endpoint import ZmqServer


def echo(input_json: dict) -> dict:
    return input_json


ECHO_SCHEMA = {
    "type": "object",
    "properties": {"message": {"type": "string"}, },
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
