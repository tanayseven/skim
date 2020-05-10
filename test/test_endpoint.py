from threading import Thread

import pytest
import zmq

from skim.endpoint import ZmqServer


def echo(input_json: dict) -> dict:
    return input_json


ECHO_SCHEMA = {
    "type": "object",
    "properties": {"message": {"type": "string"},},
    "required": ["message"],
}


@pytest.fixture
def zmq_client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    yield socket


@pytest.fixture
def zmq_server():
    server = ZmqServer(transformer=echo, validation_schema=ECHO_SCHEMA)
    server_thread = Thread(target=server.start, daemon=True)
    server_thread.start()
    yield
    server.stop()
    server_thread.join()


@pytest.mark.skip
def test_connection_echo_success(zmq_client, zmq_server):
    # given
    _ = zmq_server

    # when
    message = {"message": "Something"}
    zmq_client.send_json(message)

    # then
    received_message = zmq_client.recv_json()
    assert received_message == message


@pytest.mark.skip
def test_connection_echo_failure(zmq_client, zmq_server):
    # given
    _ = zmq_server

    # when
    message = {"text": "Something"}
    zmq_client.send_json(message)

    # then
    received_message = zmq_client.recv_json()
    assert received_message["success"] == "no"
    assert "message" in received_message
