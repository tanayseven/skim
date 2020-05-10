from typing import List

from waiting import wait

client_message_queue: List[dict] = []
server_message_queue: List[dict] = []


class FakeSocket:
    def __init__(self):
        self._receive_from_queue = client_message_queue
        self._sending_to_queue = server_message_queue

    def bind(self, *args, **kwargs):
        self._receive_from_queue = server_message_queue
        self._sending_to_queue = client_message_queue

    def send_json(self, obj: dict):
        self._sending_to_queue.append(obj)

    def recv_json(self, *args, **kwargs) -> dict:
        wait(
            lambda: len(self._receive_from_queue),
            sleep_seconds=(1, 4),
            timeout_seconds=8,
        )
        return self._receive_from_queue.pop(0)


class FakeContext:
    def socket(self, *args, **kwargs):
        return FakeSocket()
