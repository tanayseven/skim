from typing import List

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
