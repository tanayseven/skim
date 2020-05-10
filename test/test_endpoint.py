import pytest
import zmq

from test.fake_zmq import FakeSocket
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


class FakeContext:
    def socket(self, *args, **kwargs):
        return FakeSocket()


@pytest.fixture(autouse=True)
def zmq_server_patch(monkeypatch):
    monkeypatch.setattr(zmq, "Context", FakeContext)


def test_connection_echo_success(zmq_client):
    # given
    zmq_server = ZmqServer(transformer=echo, validation_schema=ECHO_SCHEMA)

    # when
    message = {"message": "Something"}
    zmq_client.send_json(message)
    zmq_server.process_message()

    # then
    received_message = zmq_client.recv_json()
    assert received_message == message


def test_connection_echo_failure(zmq_client):
    # given
    zmq_server = ZmqServer(transformer=echo, validation_schema=ECHO_SCHEMA)

    # when
    message = {"text": "Something"}
    zmq_client.send_json(message)
    zmq_server.process_message()

    # then
    received_message = zmq_client.recv_json()
    assert received_message["success"] == "no"
    assert "message" in received_message
